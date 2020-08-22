from typing import Set, Iterable, Any

from pygame import Surface, display
from src.actions import MovementAction, RotateAction, ActionQuit
from src.entity import Entity
from src.input_handlers import MainEventHandler
from src.render_functions import get_rotated_image

tile_size = 32


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: MainEventHandler, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.handle_events(event, self.player.facing)
        
            if action is None:
                continue
        
            if isinstance(action, RotateAction):
                self.player.rotate(action.rotate)
        
            elif isinstance(action, MovementAction):
                self.player.move()
        
            elif isinstance(action, ActionQuit):
                raise SystemExit()
        
    def render(self, main_surface: Surface) -> None:
        main_surface.fill((50, 50, 200))
        for entity in self.entities:
            main_surface.blit(get_rotated_image(entity.icon, entity.facing),
                              (entity.x, entity.y + ((entity.x // tile_size) % 2) * tile_size // 2))

        display.flip()
