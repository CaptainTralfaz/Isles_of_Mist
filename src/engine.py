from __future__ import annotations

import random
from typing import Dict, TYPE_CHECKING

from pygame import Surface, time

from actions.move.movement import MovementAction
from camera import Camera
from constants.constants import time_tick
from constants.enums import GameStates
from custom_exceptions import Impossible
from event_handlers.cargo_config import CargoConfigurationHandler
from event_handlers.crew_config import CrewConfigurationHandler
from event_handlers.main_game import MainEventHandler
from event_handlers.merchant import MerchantHandler
from event_handlers.player_dead import GameOverEventHandler
from event_handlers.weapon_config import WeaponConfigurationHandler
from message_log import MessageLog
from render.cargo import cargo_render
from render.controls import control_panel_render
from render.crew import crew_render
from render.entity_info import render_entity_info
from render.merchant import merchant_render
from render.mini_map import mini_map_render
from render.smithy import smithy_render
from render.status_panel import status_panel_render
from render.viewport import viewport_render
from render.weapons import weapon_render
from time_of_day import Time
from ui import DisplayInfo

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap


class Engine:
    game_map: GameMap
    
    def __init__(self, player: Entity,
                 ui_layout: DisplayInfo,
                 seed: int = None,
                 message_log: MessageLog = None,
                 time_of_day: Time = None,
                 camera: Camera = None,
                 game_state: GameStates = None):
        self.event_handler: MainEventHandler = MainEventHandler(self)
        self.player = player
        self.seed = random.randint(0, 10000) if seed is None else seed  # 8617
        self.mouse_location = (0, 0)
        self.ui_layout = ui_layout
        self.message_log = MessageLog(parent=self,
                                      height=self.ui_layout.display_height) if message_log is None else message_log
        self.clock = time.Clock()
        self.time = Time() if time_of_day is None else time_of_day
        self.key_mod = None
        self.camera = Camera() if camera is None else camera
        self.game_state = GameStates.ACTION if game_state is None else game_state
        
        random.seed(self.seed)
        print(self.seed)
    
    def to_json(self) -> Dict:
        return {
            'game_state': self.game_state.value,
            'time': self.time.to_json(),
            'seed': self.seed,
            'camera': self.camera.to_json(),
            'message_log': self.message_log.to_json(),
        }
    
    @staticmethod
    def from_json(player, ui_layout, json_data) -> Engine:
        game_state = GameStates(json_data.get('game_state'))
        time_of_day = Time.from_json(json_data.get('time'))
        seed = json_data.get('seed')
        camera = Camera.from_json(json_data.get('camera'))
        message_log = MessageLog.from_json(json_data.get('message_log'))
        return Engine(player=player, ui_layout=ui_layout, seed=seed, message_log=message_log,
                      time_of_day=time_of_day, camera=camera, game_state=game_state)
    
    def get_handler(self):
        if self.game_state == GameStates.ACTION:
            self.event_handler = MainEventHandler(self)
        elif self.game_state == GameStates.WEAPON_CONFIG:
            self.event_handler = WeaponConfigurationHandler(self)
        elif self.game_state == GameStates.CREW_CONFIG:
            self.event_handler = CrewConfigurationHandler(self)
        elif self.game_state == GameStates.CARGO_CONFIG:
            self.event_handler = CargoConfigurationHandler(self)
        elif self.game_state == GameStates.PLAYER_DEAD:
            self.event_handler = GameOverEventHandler(self)
        elif self.game_state in [GameStates.MERCHANT, GameStates.SMITHY]:
            self.event_handler = MerchantHandler(self)
        # elif self.game_state == GameStates.SMITHY:
        #     self.event_handler = SmithyHandler(self)
        # # elif self.game_state == GameStates.UPGRADES:
        #     self.event_handler = UpgradeHandler(self)
    
    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            if entity.is_alive and entity.ai is not None:
                try:
                    entity.ai.perform()
                except Impossible:
                    pass
    
    def handle_bonus_movement(self) -> None:
        if self.player.sails.raised:
            try:
                MovementAction(entity=self.player).perform()
            except Impossible:
                pass
    
    def handle_weather(self):
        self.time.roll_min(time_tick)
        self.game_map.weather.roll_weather()
        self.game_map.weather.roll_wind()
        self.game_map.weather.roll_mist(self.game_map)
    
    def render_all(self, main_surface: Surface) -> None:
        mini_map_render(game_map=self.game_map, main_display=main_surface, ui_layout=self.ui_layout)
        
        status_panel_render(console=main_surface, entity=self.player, weather=self.game_map.weather, time=self.time,
                            ui_layout=self.ui_layout)
        
        control_panel_render(console=main_surface, key_mod=self.key_mod, game_state=self.game_state,
                             player=self.player, ui_layout=self.ui_layout, sky=self.time.get_sky_color)
        
        # viewport/messages depending on mouse
        if self.ui_layout.in_messages(self.mouse_location[0], self.mouse_location[1]):
            self.message_log.render_max(console=main_surface, ui_layout=self.ui_layout)
        else:
            self.message_log.render(console=main_surface, ui_layout=self.ui_layout)
            if self.game_state in [GameStates.ACTION, GameStates.PLAYER_DEAD]:
                self.camera.update(self.player)
                viewport_render(game_map=self.game_map, main_display=main_surface, weather=self.game_map.weather,
                                ui_layout=self.ui_layout, camera=self.camera)
                if self.ui_layout.in_viewport(self.mouse_location[0], self.mouse_location[1]):
                    render_entity_info(console=main_surface,
                                       game_map=self.game_map,
                                       player=self.player,
                                       mouse_x=self.mouse_location[0] - self.ui_layout.mini_width,
                                       mouse_y=self.mouse_location[1],
                                       ui=self.ui_layout)
            elif self.game_state == GameStates.CARGO_CONFIG:
                cargo_render(console=main_surface, player=self.player, time=self.time,
                             ui_layout=self.ui_layout)
            elif self.game_state == GameStates.CREW_CONFIG:
                crew_render(console=main_surface, crew=self.player.crew, time=self.time,
                            ui_layout=self.ui_layout)
            elif self.game_state == GameStates.WEAPON_CONFIG:
                weapon_render(console=main_surface, broadsides=self.player.broadsides, time=self.time,
                              ui_layout=self.ui_layout)
            elif self.game_state == GameStates.MERCHANT:
                merchant_render(console=main_surface, player=self.player, time=self.time,
                                ui_layout=self.ui_layout)
            elif self.game_state == GameStates.SMITHY:
                smithy_render(console=main_surface, player=self.player, time=self.time,
                              ui_layout=self.ui_layout)
