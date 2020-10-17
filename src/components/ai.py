from __future__ import annotations

from typing import TYPE_CHECKING

from actions.attack.melee import MeleeAction
from actions.base.base import Action
from actions.move.movement import MovementAction
from actions.move.rotate import RotateAction
from actions.move.wander import WanderAction
from utilities import get_distance, closest_rotation, get_neighbor

if TYPE_CHECKING:
    from entity import Entity
    from typing import Dict


class BaseAI(Action):
    
    def to_json(self) -> None:
        raise NotImplementedError()
    
    def perform(self) -> None:
        raise NotImplementedError()


class NeutralEnemy(BaseAI):
    def __init__(self, entity: Entity):
        super().__init__(entity)
    
    def to_json(self) -> Dict:
        return {
            'ai_cls': self.__class__.__name__
        }
    
    @staticmethod
    def from_json(json_data: Dict) -> Dict:
        ai_cls = json_data.get('ai_cls')
        return ai_cls
    
    def perform(self) -> bool:
        """
        Neutral Enemy will do nothing but wander randomly, even if attacked
        """
        return WanderAction(self.entity).perform()


class HostileEnemy(BaseAI):
    def __init__(self, entity: Entity, target=None, path=None):
        super().__init__(entity)
        self.target = target
        if path is None:
            self.path = []
        else:
            self.path = path
    
    def to_json(self) -> Dict:
        return {
            'ai_cls': self.__class__.__name__,
            'target': self.target,
            'path': self.path
        }
    
    def perform(self) -> bool:
        """
        Hostile entity will wander randomly until player is spotted, making that location its target
        Hostile entity will update target and path to target each subsequent turn player is visible
        Hostile entity will attack if adjacent
        Hostile will move or rotate toward target location if not adjacent
        If target location is reached, Hostile will revert to wandering
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
                return RotateAction(self.entity, closest_rotation(self.target,
                                                                  self.entity.x,
                                                                  self.entity.y,
                                                                  self.entity.facing
                                                                  )).perform()
        # no path left - reset our variables
        else:
            self.target = None
            self.path = []
        # if none of the above works, just wander...
        return WanderAction(self.entity).perform()


class HostileFlyingEnemy(BaseAI):
    def __init__(self, entity: Entity, target=None, distance_map=None):
        super().__init__(entity)
        self.target = target
        if distance_map is None:
            self.distance_map = {}
        else:
            self.distance_map = distance_map.distance_map_from_json(distance_map)
    
    def to_json(self) -> Dict:
        return {
            'ai_cls': self.__class__.__name__,
            'target': self.target,
            'distance_map': self.dist_map_to_json()
        }
    
    def dist_map_to_json(self):
        keys = []
        values = []
        for key in self.distance_map.keys():
            keys.append(key)
            values.append(self.distance_map[key])
        return {
            'keys': keys,
            'values': values
        }
    
    @staticmethod
    def distance_map_from_json(json_dist_map):
        distance_map = {}
        keys = json_dist_map['keys']
        values = json_dist_map['values']
        for i in range(len(keys)):
            distance_map[keys[i]] = values[i]
        return distance_map
    
    def perform(self) -> bool:
        """
        Hostile flyer will wander randomly until player is spotted, making that location its target
        Hostile entity will update target distance map each subsequent turn player is visible
        Hostile will move or rotate toward target location according to distance map
        If target location is reached, Hostile will revert wandering randomly
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
                if self.distance_map.get(neighbor) < shortest:
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
                return RotateAction(self.entity, closest_rotation(target,
                                                                  self.entity.x,
                                                                  self.entity.y,
                                                                  self.entity.facing
                                                                  )).perform()
        return WanderAction(self.entity).perform()


ai_class = {
    'NeutralEnemy': NeutralEnemy,
    'HostileEnemy': HostileEnemy,
    'HostileFlyingEnemy': HostileFlyingEnemy,
}
