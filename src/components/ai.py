from __future__ import annotations

from typing import TYPE_CHECKING

from actions import Action, MeleeAction, RotateAction, MovementAction, WanderAction
from utilities import get_distance, closest_rotation, get_neighbor

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
        
        if len(self.path) > 0:
            self.target = self.path[-1]  # where we actually want to go
            # if we're facing the target hex:
            if get_neighbor(self.entity.x, self.entity.y, self.entity.facing) == self.target:
                # just move forward
                self.path.pop()  # consume the target hex from the path
                return MovementAction(self.entity).perform()  # and move to it
            # can't move forward, so lets rotate
            else:
                return RotateAction(self.entity, closest_rotation(self.target, self.entity)).perform()
        
        # no path left - reset our variables
        else:
            self.target = None
            self.path = []
        # if none of the above works, just wander...
        return WanderAction(self.entity).perform()


class HostileFlyingEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.target = None
        self.distance_map = {}
    
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
            self.distance_map = {}
            return WanderAction(self.entity).perform()
        
        # in player in view, set new target location at player's location and generate distance map
        if (self.engine.player.x, self.engine.player.y) in self.entity.view.fov:
            target = (self.engine.player.x, self.engine.player.y)
            
            # we have a target hex, find a path
            self.distance_map = self.engine.game_map.get_distance_map(self.entity.x,
                                                                      self.entity.y,
                                                                      target[0],
                                                                      target[1],
                                                                      self.entity.elevations)
            distance = get_distance(self.entity.x, self.entity.y, target[0], target[1])
            # if in view and close enough to melee attack
            if distance <= 1:
                return MeleeAction(self.entity).perform()
            # TODO: add ranged weapons
            # elif distance <= entity.ranged_attacks and entity can_attack:
            #     return RangedAction
        
        if len(self.distance_map.keys()) > 0:
            # find shortest distance neighbor
            shortest = self.distance_map[self.entity.x, self.entity.y]
            target = (self.entity.x, self.entity.y)
            for neighbor in self.engine.game_map.get_neighbors_at_elevations(self.entity.x,
                                                                             self.entity.y,
                                                                             self.entity.elevations):
                if self.distance_map[neighbor] < shortest:
                    target = neighbor
                    shortest = self.distance_map[neighbor]
            
            # if we're facing the target hex:
            next_hex = get_neighbor(self.entity.x, self.entity.y, self.entity.facing)
            if self.engine.game_map.in_bounds(next_hex[0], next_hex[1]) \
                    and self.distance_map[next_hex] == shortest:
                # just move forward
                return MovementAction(self.entity).perform()  # and move to it
            # can't move forward, so lets rotate
            elif shortest == 0:
                self.target = None
                self.distance_map = {}
                return WanderAction(self.entity).perform()
            else:
                return RotateAction(self.entity, closest_rotation(target, self.entity)).perform()
        
        return WanderAction(self.entity).perform()
