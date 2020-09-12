from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from input_handlers import MainEventHandler
from render_functions import render_bar, render_entity_info
from message_log import MessageLog
from tile import tile_size

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap


class Engine:
    game_map: GameMap
    
    def __init__(self, player: Actor):
        self.event_handler: MainEventHandler = MainEventHandler(self)
        self.player = player
        self.mouse_location = (0, 0)
        self.message_log = MessageLog()

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            if entity.ai:
                entity.ai.perform()
    
    def render(self, main_surface: Surface) -> None:
        self.game_map.render(main_surface)

        self.message_log.render(console=main_surface,
                                x=0,
                                y=self.game_map.height * tile_size - 16,
                                width=self.game_map.width * tile_size - 10,
                                height=8)
        
        health_bar = render_bar("Hull Points", self.player.fighter.hp, self.player.fighter.max_hp, 200)
        main_surface.blit(health_bar, (10, 10))
        
        render_entity_info(main_surface,
                           self.game_map,
                           self.player.view.fov,
                           self.mouse_location[0],
                           self.mouse_location[1])
