from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

from actions import Action, MeleeAction, RotateAction, MovementAction, WanderAction
from utilities import get_distance, get_neighbor

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action):
    
    def perform(self) -> None:
        raise NotImplementedError()


class NeutralEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
    
    def perform(self) -> bool:
        return WanderAction(self.entity).perform()


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.target = None
        self.path = []
    
    def perform(self) -> bool:
        """
        Hostile entity will wander randomly until player is spotted, making that location its target
        Hostile entity will update target each subsequent turn player is visible
        Hostile will move or rotate toward target location
        if target location is empty, Hostile will wander
        :return: action -> bool
        """
        # if player is in port, stop hunting
        if (self.engine.player.x, self.engine.player.y) == self.engine.game_map.port:
            self.path = []
            return WanderAction(self.entity).perform()
        
        # in player in view, set new target location at player's location and generate distance map
        if (self.engine.player.x, self.engine.player.y) in self.entity.view.fov:
            self.target = (self.engine.player.x, self.engine.player.y)
            # we have a target hex, find a path
            self.path = self.engine.game_map.get_path(self.entity.x,
                                                      self.entity.y,
                                                      self.target[0],
                                                      self.target[1],
                                                      self.entity.elevations)
            distance = get_distance(self.entity.x, self.entity.y, self.target[0], self.target[1])
            # if in view and close enough to melee attack
            if distance <= 1:
                return MeleeAction(self.entity).perform()
            # TODO: add ranged weapons
            # elif distance <= entity.ranged_attacks and entity can_attack:
            #     return RangedAction
        
        # if we still have a path, target the next hex in the path
        if len(self.path) > 0:
            self.target = self.path.pop()  # where we actually want to go
            
            # if we're facing the target hex:
            if get_neighbor(self.entity.x, self.entity.y, self.entity.facing) == self.target:
                # just move forward
                return MovementAction(self.entity).perform()
                
            # can't move forward, so lets rotate
            facing_left = self.entity.facing
            for turns in range(0, 5):
                facing_left -= 1
                if facing_left < 0:
                    facing_left = 5
                left_hex = get_neighbor(self.entity.x, self.entity.y, facing_left)
                if left_hex == self.target:
                    if turns in [0, 1]:  # left is shorter
                        return RotateAction(self.entity, -1).perform()
                    elif turns in [3, 4]:  # right is shorter
                        return RotateAction(self.entity, 1).perform()
                    else:  # directly behind - turn randomly
                        return RotateAction(self.entity, choice([-1, 1])).perform()
        # no path left - reset our variables
        else:
            self.target = None
            self.path = []
        # if none of the above works, just wander...
        return WanderAction(self.entity).perform()
