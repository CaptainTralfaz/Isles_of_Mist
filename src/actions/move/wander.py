from __future__ import annotations

from random import choice, randint
from typing import TYPE_CHECKING

from actions.base import Action
from actions.move.movement import MovementAction
from actions.move.rotate import RotateAction

if TYPE_CHECKING:
    from entity import Actor


class WanderAction(Action):
    def __init__(self, entity: Actor):
        """
        randomly chooses between rotating left, rotating right, or attempting to move forward
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        decision = randint(-1, 1)
        x, y = self.entity.get_next_hex()
        if decision == 0 \
                and self.engine.game_map.in_bounds(x, y) \
                and self.engine.game_map.can_move_to(x, y, self.entity.elevations):
            return MovementAction(self.entity).perform()
        else:
            decision = choice([-1, 1])
            return RotateAction(self.entity, decision).perform()
