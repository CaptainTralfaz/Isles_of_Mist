from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface, time

from action.move.movement import MovementAction
from camera import Camera
from constants import time_tick
from custom_exceptions import Impossible
from enums import GameStates
from event_handlers.cargo_config import CargoConfigurationHandler
from event_handlers.crew_config import CrewConfigurationHandler
from event_handlers.main_game import MainEventHandler
from event_handlers.player_dead import GameOverEventHandler
from event_handlers.weapon_config import WeaponConfigurationHandler
from message_log import MessageLog
from render.cargo import cargo_render
from render.controls import control_panel_render
from render.crew import crew_render
from render.entity_info import render_entity_info
from render.mini_map import mini_map_render
from render.status_panel import status_panel_render
from render.viewport import viewport_render
from render.weapons import weapon_render
from ui import DisplayInfo
from weather import Weather, Time

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap


class Engine:
    game_map: GameMap
    
    def __init__(self, player: Actor, ui_layout: DisplayInfo):
        self.event_handler: MainEventHandler = MainEventHandler(self)
        self.player = player
        self.mouse_location = (0, 0)
        self.message_log = MessageLog(parent=self)
        self.ui_layout = ui_layout
        self.clock = time.Clock()
        self.weather = Weather(parent=self, width=ui_layout.viewport_width, height=ui_layout.viewport_height)
        self.time = Time()
        self.key_mod = None
        self.camera = Camera()
        self.game_state = GameStates.ACTION

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

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            if entity.is_alive and entity.ai:
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
        self.weather.roll_weather()
        self.weather.roll_wind()
        self.weather.roll_mist(self.game_map)
    
    def render_all(self, main_surface: Surface) -> None:
        mini_map_render(game_map=self.game_map, main_display=main_surface, ui_layout=self.ui_layout)
        
        status_panel_render(console=main_surface, entity=self.player, weather=self.weather, time=self.time,
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
                viewport_render(game_map=self.game_map, main_display=main_surface, weather=self.weather,
                                ui_layout=self.ui_layout, camera=self.camera)
                if self.ui_layout.in_viewport(self.mouse_location[0], self.mouse_location[1]):
                    render_entity_info(console=main_surface,
                                       game_map=self.game_map,
                                       player=self.player,
                                       mouse_x=self.mouse_location[0] - self.ui_layout.mini_width,
                                       mouse_y=self.mouse_location[1],
                                       ui=self.ui_layout)
            elif self.game_state == GameStates.CARGO_CONFIG:
                cargo_render(console=main_surface, cargo=self.player.cargo, time=self.time,
                             ui_layout=self.ui_layout)
            elif self.game_state == GameStates.CREW_CONFIG:
                crew_render(console=main_surface, crew=self.player.crew, time=self.time,
                            ui_layout=self.ui_layout)
            elif self.game_state == GameStates.WEAPON_CONFIG:
                weapon_render(console=main_surface, broadsides=self.player.broadsides, time=self.time,
                              ui_layout=self.ui_layout)
