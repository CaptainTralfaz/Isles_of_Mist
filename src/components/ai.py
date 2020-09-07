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
        target = self.engine.player
        if (target.x, target.y) in self.entity.view.fov:
            print(f"{self.entity.name} says HI")
        return WanderAction(self.entity).perform()


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.current_target_x = None
        self.current_target_y = None
    
    def perform(self) -> bool:
        """
        Hostile entity will wander randomly until player is spotted, making that location its target
        Hostile entity will update target each subsequent turn player is visible
        Hostile will move or rotate toward target location
        if target location is empty, Hostile will patrol around the edge that location
        :return: action -> bool
        """
        # in view, set new target location
        if (self.engine.player.x, self.engine.player.y) in self.entity.view.fov:
            print(f"{self.entity.name} updating target: ({self.engine.player.x}, {self.engine.player.y})")
            self.current_target_x = self.engine.player.x
            self.current_target_y = self.engine.player.y
            
            distance = get_distance(self.entity.x, self.entity.y, self.current_target_x, self.current_target_y)
            # melee attack if close enough
            if distance < 2:
                return MeleeAction(self.entity).perform()
        
        # have a target location: find path, then move or rotate
        if self.current_target_x is not None and self.current_target_y is not None:
            
            if self.entity.flying:
                distance_map = self.engine.game_map.gen_flying_distance_map(self.current_target_x,
                                                                            self.current_target_y)
            else:
                distance_map = self.engine.game_map.gen_sail_distance_map(self.current_target_x,
                                                                          self.current_target_y)
            
            neighbors = self.engine.game_map.get_neighbors(self.entity.x, self.entity.y)
            shortest_dist_coords = []
            shortest_dist = get_distance(self.entity.x, self.entity.y,
                                         self.current_target_x, self.current_target_y)
            
            # print(neighbors)
            for neighbor in neighbors:
                neighbor_dist = distance_map.get((neighbor[0], neighbor[1]))
                if neighbor_dist is not None:
                    if neighbor_dist < shortest_dist:
                        shortest_dist_coords = [neighbor]
                        shortest_dist = neighbor_dist
                    elif neighbor_dist == shortest_dist:
                        shortest_dist_coords.append(neighbor)
            
            facing_x, facing_y = get_neighbor(self.entity.x, self.entity.y, self.entity.facing)
            can_move_to = False
            if self.entity.game_map.in_bounds(facing_x, facing_y):
                if self.entity.flying:
                    can_move_to = self.entity.game_map.can_fly_to(facing_x, facing_y)
                else:
                    can_move_to = self.entity.game_map.can_sail_to(facing_x, facing_y)
            if distance_map.get((facing_x, facing_y)) == shortest_dist \
                    and can_move_to:
                return MovementAction(self.entity).perform()
            
            left_shortest = 3
            facing_left = self.entity.facing
            for left_count in range(1, 3):
                facing_left -= 1
                if facing_left < 0:
                    facing_left = 5
                left_x, left_y = get_neighbor(self.entity.x, self.entity.y, facing_left)
                left_current = distance_map.get((left_x, left_y))
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
                right_current = distance_map.get((right_x, right_y))
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
        
        # this is hit if current_target_x and current_target_y are None
        # currently, this is never reset - enemies are unable to actually reach their target coordinates,
        #  and will patrol around their target location instead
        assert self.current_target_x is None
        assert self.current_target_y is None
        return WanderAction(self.entity).perform()
