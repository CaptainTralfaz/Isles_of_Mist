from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from input_handlers import MainEventHandler

if TYPE_CHECKING:
    from entity import Entity, Actor
    from game_map import GameMap


class Engine:
    game_map: GameMap
    
    def __init__(self, player: Actor):
        self.event_handler: MainEventHandler = MainEventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            if entity.ai:
                entity.ai.perform()
    
    def render(self, main_surface: Surface) -> Surface:
        self.game_map.render(main_surface)
        
        return main_surface
