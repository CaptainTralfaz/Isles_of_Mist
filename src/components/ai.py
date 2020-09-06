from __future__ import annotations

from typing import TYPE_CHECKING
from random import randint, choice
from actions import Action, WaitAction, RotateAction, MovementAction
from utilities import get_distance, get_neighbor

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
        decision = randint(-1, 1)
        target = self.engine.player
        if (target.x, target.y) in self.entity.view.fov:
            print("{} says HI".format(self.entity.name))
        if decision in [-1, 1]:
            return RotateAction(self.entity, decision).perform()
        elif decision == 0:
            return MovementAction(self.entity).perform()
        else:
            return WaitAction(self.entity).perform()


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.current_target_x = None
        self.current_target_y = None

    def perform(self) -> bool:
        
        if (self.engine.player.x, self.engine.player.y) in self.entity.view.fov:
            print("{} updating target: ({}, {})".format(self.entity.name, self.engine.player.x, self.engine.player.y))
            self.current_target_x = self.engine.player.x
            self.current_target_y = self.engine.player.y
            
            distance = get_distance(self.entity.x, self.entity.y, self.current_target_x, self.current_target_y)
            # melee attack if close enough
            if distance < 2:
                print("{} bites you!".format(self.entity.name))
                return True  # return MeleeAction(self.entity, self.target).perform()
            
        # have a target, find path, then move or rotate
        if self.current_target_x is not None and self.current_target_y is not None:
            # print("({}, {}) -> ({}, {})".format(self.entity.x, self.entity.y, self.current_target_x, self.current_target_y))

            sail_distance_map = self.engine.game_map.gen_sail_distance_map(self.current_target_x, self.current_target_y)
            
            neighbors = self.engine.game_map.get_neighbors(self.entity.x, self.entity.y)
            shortest_dist_coords = []
            shortest_dist = get_distance(self.entity.x, self.entity.y, self.current_target_x, self.current_target_y)
            # print("origin ({}, {}) shortest dist: {}".format(self.entity.x, self.entity.y, shortest_dist))
            # print("target ({}, {})".format(self.current_target_x, self.current_target_y))

            # print(neighbors)
            for neighbor in neighbors:
                neighbor_dist = sail_distance_map.get((neighbor[0], neighbor[1]))
                # print("neighbor ({}, {}) dist: {}".format(neighbor[0], neighbor[1], neighbor_dist))
                if neighbor_dist is not None:
                    if neighbor_dist < shortest_dist:
                        shortest_dist_coords = [neighbor]
                        shortest_dist = neighbor_dist
                    elif neighbor_dist == shortest_dist:
                        shortest_dist_coords.append(neighbor)
            
            facing_x, facing_y = get_neighbor(self.entity.x, self.entity.y, self.entity.facing)
            if sail_distance_map.get((facing_x, facing_y)) == shortest_dist \
                    and self.entity.game_map.can_sail_to(facing_x, facing_y):
                return MovementAction(self.entity).perform()
            
            left_shortest = 3
            facing_left = self.entity.facing
            for left_count in range(1, 3):
                facing_left -= 1
                if facing_left < 0:
                    facing_left = 5
                left_x, left_y = get_neighbor(self.entity.x, self.entity.y, facing_left)
                left_current = sail_distance_map.get((left_x, left_y))
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
                right_current = sail_distance_map.get((right_x, right_y))
                if right_current is not None \
                        and right_current == shortest_dist:
                    right_shortest = right_count
                
            if left_shortest == right_shortest:
                # rotate randomly
                # print("{} rotates randomly".format(self.entity.name))
                return RotateAction(self.entity, choice([-1, 1])).perform()
            elif left_shortest < right_shortest:
                return RotateAction(self.entity, -1).perform()
            elif right_shortest < left_shortest:
                return RotateAction(self.entity, 1).perform()

            # TODO - this code never gets reached... currently AI just circles the target for some reason...
            #       which is fine :)  FEATURE > BUG, right??
            # print("({}, {}) -> ({}, {})".format(self.entity.x, self.entity.y,
            #                                     self.current_target_x, self.current_target_y))
            # if ((self.engine.player.x, self.engine.player.y) not in self.entity.view.fov) \
            #         and (self.current_target_x == self.entity.x) \
            #         and (self.current_target_y == self.entity.y):
            #     self.current_target_x = None
            #     self.current_target_y = None
            #     print("{} stops following you".format(self.entity.name))

        # self.current_target_x = None
        # self.current_target_y = None
        # print("{} wanders...".format(self.entity.name))
        decision = randint(-1, 1)
        if decision in [-1, 1]:
            return RotateAction(self.entity, decision).perform()
        elif decision == 0:
            return MovementAction(self.entity).perform()
        else:
            return WaitAction(self.entity).perform()
