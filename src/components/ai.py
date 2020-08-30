from __future__ import annotations

from typing import TYPE_CHECKING
from random import randint
from actions import Action, WaitAction, RotateAction, MovementAction

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action):
    
    def perform(self) -> None:
        raise NotImplementedError()


class NeutralEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
    
    # Wander Action
    def perform(self) -> bool:
        choice = randint(-1, 1)
        if choice in [-1, 1]:
            return RotateAction(self.entity, choice).perform()
        elif choice == 0:
            return MovementAction(self.entity).perform()
        else:
            return WaitAction(self.entity).perform()
