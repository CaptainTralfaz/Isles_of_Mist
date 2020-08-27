from typing import Iterable, Any

from pygame import Surface

from entity import Entity
from game_map import GameMap
from input_handlers import MainEventHandler


class Engine:
    def __init__(self, event_handler: MainEventHandler, game_map: GameMap, player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.handle_events(event, self.player.facing)
            
            if action is None:
                continue
            
            action.perform(self, self.player)
            self.handle_enemy_turns()
            # update FOV

    def render(self, main_surface: Surface) -> Surface:
        self.game_map.render(main_surface)

        return main_surface
