from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

from actions import Action, MeleeAction, RotateAction, MovementAction, WanderAction
from constants import move_elevations
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
        self.target_x = None
        self.target_y = None
        self.distance_map = None
    
    def perform(self) -> bool:
        """
        Hostile entity will wander randomly until player is spotted, making that location its target
        Hostile entity will update target each subsequent turn player is visible
        Hostile will move or rotate toward target location
        if target location is empty, Hostile will patrol around the edge that location
        :return: action -> bool
        """
        # if player is in port, stop hunting
        if (self.engine.player.x, self.engine.player.y) == self.engine.game_map.port:
            self.target_x = None
            self.target_y = None
            return WanderAction(self.entity).perform()
        
        # in player in view, set new target location at player's location and generate distance map
        if (self.engine.player.x, self.engine.player.y) in self.entity.view.fov:
            self.target_x = self.engine.player.x
            self.target_y = self.engine.player.y
            self.distance_map = self.engine.game_map.gen_distance_map(self.target_x,
                                                                      self.target_y,
                                                                      self.entity.elevations)
            
            distance = get_distance(self.entity.x, self.entity.y, self.target_x, self.target_y)
            # print(f"{self.entity.name} is {distance} hex(es) to player")
            if distance <= 1:
                return MeleeAction(self.entity).perform()
            # TODO: add ranged weapons
            # elif distance <= entity.ranged_attacks and entity can_attack:
            #     return RangedAction
        
        if self.target_x is not None and self.target_y is not None:
            distance = get_distance(self.entity.x, self.entity.y, self.target_x, self.target_y)
            # print(f"{self.entity.name} is {distance} hex(es) to target")
            if (self.engine.player.x, self.engine.player.y) not in self.entity.view.fov \
                    and (self.engine.game_map.terrain[self.target_x][self.target_y].elevation
                         not in self.entity.elevations or (distance <= 1)):
                self.target_x = None
                self.target_y = None
                self.distance_map = None
                # print(f"{self.entity.name} calls off the pursuit")
                return WanderAction(self.entity).perform()
            
            else:
                neighbors = self.engine.game_map.get_neighbors_at_elevations(self.entity.x, self.entity.y,
                                                                             move_elevations['all'])
                if self.entity.game_map.port in neighbors:
                    neighbors.remove(self.entity.game_map.port)
                shortest_dist_coords = []
                shortest_dist = get_distance(self.entity.x, self.entity.y, self.target_x, self.target_y)
                
                for neighbor in neighbors:
                    neighbor_dist = self.distance_map.get((neighbor[0], neighbor[1]))
                    if neighbor_dist is not None:
                        if neighbor_dist < shortest_dist:
                            shortest_dist_coords = [neighbor]
                            shortest_dist = neighbor_dist
                        elif neighbor_dist == shortest_dist:
                            shortest_dist_coords.append(neighbor)
                
                facing_x, facing_y = get_neighbor(self.entity.x, self.entity.y, self.entity.facing)
                can_move_to = False
                if self.entity.game_map.in_bounds(facing_x, facing_y):
                    can_move_to = self.entity.game_map.can_move_to(facing_x, facing_y, self.entity.elevations)
                if self.distance_map.get((facing_x, facing_y)) == shortest_dist and can_move_to:
                    return MovementAction(self.entity).perform()
                
                left_shortest = 3
                facing_left = self.entity.facing
                for left_count in range(1, 3):
                    facing_left -= 1
                    if facing_left < 0:
                        facing_left = 5
                    left_x, left_y = get_neighbor(self.entity.x, self.entity.y, facing_left)
                    left_current = self.distance_map.get((left_x, left_y))
                    if left_current is not None \
                            and left_current == shortest_dist:
                        left_shortest = left_count
                
                right_shortest = 3
                facing_right = self.entity.facing
                for right_count in range(1, 3):
                    facing_right += 1
                    if facing_right > 5:
                        facing_right = 0
                    right_x, right_y = get_neighbor(self.entity.x, self.entity.y, facing_right)
                    right_current = self.distance_map.get((right_x, right_y))
                    if right_current is not None \
                            and right_current == shortest_dist:
                        right_shortest = right_count
                
                if left_shortest == right_shortest:
                    # rotate randomly
                    return RotateAction(self.entity, choice([-1, 1])).perform()
                elif left_shortest < right_shortest:
                    return RotateAction(self.entity, -1).perform()
                elif right_shortest < left_shortest:
                    return RotateAction(self.entity, 1).perform()
        
        return WanderAction(self.entity).perform()
