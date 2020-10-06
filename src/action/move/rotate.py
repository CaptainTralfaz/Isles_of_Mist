from __future__ import annotations

from typing import TYPE_CHECKING

from action.base import Action

if TYPE_CHECKING:
    from entity import Actor


class RotateAction(Action):
    def __init__(self, entity: Actor, direction: int):
        """
        rotates the entity in the given direction
        :param entity: acting Entity
        :param direction: int left (-1) or right (1)
        """
        super().__init__(entity)
        self.direction = direction
    
    def perform(self) -> bool:
        self.entity.rotate(self.direction)
        return True
