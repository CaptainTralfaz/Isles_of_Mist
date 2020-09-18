from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from custom_exceptions import Impossible
from input_handlers import MainEventHandler
from message_log import MessageLog
from render_functions import render_entity_info, status_panel_render
from ui import DisplayInfo

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap


class Engine:
    game_map: GameMap
    
    def __init__(self, player: Actor, ui_layout: DisplayInfo):
        self.event_handler: MainEventHandler = MainEventHandler(self)
        self.player = player
        self.mouse_location = (0, 0)
        self.message_log = MessageLog()
        self.ui_layout = ui_layout
    
    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except Impossible:
                    pass
    
    def render(self, main_surface: Surface) -> None:
        self.game_map.render(main_display=main_surface, ui_layout=self.ui_layout)
        
        self.game_map.render_mini(main_display=main_surface, ui_layout=self.ui_layout)
        
        self.message_log.render(console=main_surface, ui_layout=self.ui_layout)
        
        status_panel_render(console=main_surface, entity=self.player, ui_layout=self.ui_layout)
        
        # stuff under mouse
        if self.ui_layout.mini_width <= self.mouse_location[0] < self.ui_layout.display_width - 1 \
                and 0 < self.mouse_location[1] < self.ui_layout.viewport_height - 1:
            render_entity_info(console=main_surface,
                               game_map=self.game_map,
                               player=self.player,
                               mouse_x=self.mouse_location[0] - self.ui_layout.mini_width,
                               mouse_y=self.mouse_location[1],
                               offset=self.ui_layout.mini_width)
