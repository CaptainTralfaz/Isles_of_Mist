from __future__ import annotations

from typing import TYPE_CHECKING
from random import randint
from actions import Action, WaitAction, RotateAction, MovementAction
from utilities import get_distance

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
        target = self.engine.player
        if (target.x, target.y) in self.entity.view.fov:
            print("{} says HI".format(self.entity.name))
        if choice in [-1, 1]:
            return RotateAction(self.entity, choice).perform()
        elif choice == 0:
            return MovementAction(self.entity).perform()
        else:
            return WaitAction(self.entity).perform()


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
    
    # Wander Action
    def perform(self) -> bool:
        target = self.engine.player
        if (target.x, target.y) in self.entity.view.fov:
            print("{} spots you!".format(self.entity.name))
            # if propulsion not on and relationship = front arc:
            #     turn propulsion on
            # else:
            #     rotate toward target
        distance = get_distance(self.entity.x, self.entity.y, target.x, target.y)
        if distance < 2:
            print("{} bites you!".format(self.entity.name))
            # melee attack
        # else:
        #    get path
        
        
        else:
            choice = randint(-1, 1)
            if choice in [-1, 1]:
                return RotateAction(self.entity, choice).perform()
            elif choice == 0:
                return MovementAction(self.entity).perform()
            else:
                return WaitAction(self.entity).perform()

# class HostileEnemy(BaseAI):
#     def __init__(self, entity: Actor):
#         super().__init__(entity)
#
#     def perform(self) -> None:
#         target = self.engine.player
#         dx = target.x - self.entity.x
#         dy = target.y - self.entity.y
#         distance = max(abs(dx), abs(dy))  # Chebyshev distance.
#
#         if self.engine.game_map.visible[self.entity.x, self.entity.y]:
#             if distance <= 1:
#                 return MeleeAction(self.entity, dx, dy).perform()
#
#             self.path = self.get_path_to(target.x, target.y)
#
#         if self.path:
#             dest_x, dest_y = self.path.pop(0)
#             return MovementAction(
#                 self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
#             ).perform()
#
#         return WaitAction(self.entity).perform()
