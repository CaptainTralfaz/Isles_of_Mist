from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

from actions.base import Action

if TYPE_CHECKING:
    from entity import Actor


class MouseMoveAction(Action):
    def __init__(self, entity: Actor, position: Tuple[int, int]):
        """
        this action simply records the current mouse x and y coordinates in the Engine
        :param entity:
        :param position:
        """
        self.x = position[0]
        self.y = position[1]
        super().__init__(entity)
    
    @property
    def position(self):
        return self.x, self.y
    
    def perform(self) -> bool:
        self.engine.mouse_location = self.position
        return False
