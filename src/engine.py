from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface, time

from actions import MovementAction
from camera import Camera
from constants import time_tick
from custom_exceptions import Impossible
from input_handlers import MainEventHandler
from message_log import MessageLog
from render_functions import render_entity_info, status_panel_render, control_panel_render, viewport_render, \
    mini_map_render
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
        self.weather = Weather(parent=self)
        self.time = Time()
        self.key_mod = None
        self.camera = Camera()
        
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
        if self.weather.wind_direction is not None:
            self.weather.roll_mist(self.game_map)
    
    def render_all(self, main_surface: Surface) -> None:
        self.camera.update(self.player)
        viewport_render(game_map=self.game_map, main_display=main_surface,
                        ui_layout=self.ui_layout, camera=self.camera)
        
        mini_map_render(game_map=self.game_map, main_display=main_surface, ui_layout=self.ui_layout)
        
        self.message_log.render(console=main_surface, ui_layout=self.ui_layout)
        
        status_panel_render(console=main_surface, entity=self.player, weather=self.weather, time=self.time,
                            ui_layout=self.ui_layout)
        
        control_panel_render(console=main_surface, status=self.key_mod, player=self.player,
                             ui_layout=self.ui_layout, sky=self.time.get_sky_color)
        
        # stuff under mouse
        if self.ui_layout.mini_width <= self.mouse_location[0] < self.ui_layout.display_width - 1 \
                and 0 < self.mouse_location[1] < self.ui_layout.viewport_height - 1:
            render_entity_info(console=main_surface,
                               game_map=self.game_map,
                               player=self.player,
                               mouse_x=self.mouse_location[0] - self.ui_layout.mini_width,
                               mouse_y=self.mouse_location[1],
                               ui=self.ui_layout)
