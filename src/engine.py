from typing import Set, Iterable, Any

from pygame import Surface

from src.entity import Entity
from src.game_map import GameMap
from src.input_handlers import MainEventHandler
from src.render_functions import get_rotated_image
from src.tile import tile_size


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: MainEventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
    
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.handle_events(event, self.player.facing)
            
            if action is None:
                continue
            
            action.perform(self, self.player)
    
    def render(self, main_surface: Surface) -> Surface:
        self.game_map.render(main_surface)
        for entity in self.entities:
            main_surface.blit(get_rotated_image(entity.icon, entity.facing),
                              (entity.x - 5, entity.y - 16 + ((entity.x // tile_size) % 2) * tile_size // 2))

        return main_surface
