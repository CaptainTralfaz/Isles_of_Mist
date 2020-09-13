from __future__ import annotations

from random import randint, choice
from typing import TYPE_CHECKING, Optional, List, Tuple

from colors import colors
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor


class Action:
    """Generic Action"""
    
    def __init__(self, entity: Actor):
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        """Return engine for this action"""
        return self.entity.parent.engine
    
    def perform(self) -> bool:
        """Perform this action with the objects needed to determine its scope.
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


# class ActionEscape(Action):
#     def perform(self) -> None:
#         raise SystemExit()


class ActionQuit(Action):
    """Action that quits the game"""
    
    def perform(self) -> None:
        raise SystemExit()


class WaitAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        self.engine.message_log.add_message(f"{self.entity.name} waits...")
        return True


class MovementAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        x, y = self.entity.get_next_hex()
        if self.entity.parent.in_bounds(x, y):
            if self.entity.flying:
                can_move = self.entity.parent.game_map.can_fly_to(x, y)
            else:
                can_move = self.entity.parent.game_map.can_sail_to(x, y)
            if can_move:
                self.entity.move()
                self.entity.view.set_fov()
                return True
            elif self.entity == self.engine.player:
                raise Impossible("Blocked")
            else:
                print(f"{self.entity.name} is blocked")
                return False


class RotateAction(Action):
    def __init__(self, entity, direction):
        super().__init__(entity)
        self.direction = direction
    
    def perform(self) -> bool:
        self.entity.rotate(self.direction)
        return True


class WanderAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        decision = randint(-1, 1)
        x, y = self.entity.get_next_hex()
        if decision == 0 \
                and self.engine.game_map.in_bounds(x, y) \
                and self.engine.game_map.can_sail_to(x, y):
            return MovementAction(self.entity).perform()
        else:
            decision = choice([-1, 1])
            return RotateAction(self.entity, decision).perform()


class MeleeAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    @property
    def target(self) -> Optional[Actor]:
        return self.engine.player
    
    def perform(self) -> bool:
        damage = self.entity.fighter.power - self.target.fighter.defense
        attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}"
        
        if damage > 0:
            self.target.fighter.hp -= damage
            
            self.engine.message_log.add_message(f"{attack_desc} for {damage} " +
                                                f"{self.target.fighter.name} damage",
                                                colors["enemy_atk"])
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage",
                                                colors["enemy_atk"])
        return True


class SplitDamageAction(Action):
    def __init__(self, entity: Actor, targets: List[Actor]):
        super().__init__(entity)
        self.targets = targets
    
    def perform(self) -> bool:
        if len(self.targets) > 0:
            split_damage = self.entity.fighter.power // len(self.targets)
            for target in self.targets:
                damage = split_damage - target.fighter.defense
                
                attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
                if damage > 0:
                    target.fighter.hp -= damage
                    self.engine.message_log.add_message(f"{attack_desc} for {damage} " +
                                                        f"{target.fighter.name} damage",
                                                        colors["player_atk"])
                else:
                    self.engine.message_log.add_message(f"{attack_desc} but does no damage",
                                                        colors["player_atk"])
            return True
        raise Impossible("No Targets")


class ArrowAction(SplitDamageAction):
    def __init__(self, entity: Actor):
        self.entity = entity
        targets = []
        neighbor_tiles = self.engine.game_map.get_neighbors(self.entity.x, self.entity.y)
        neighbor_tiles.append((entity.x, entity.y))
        for tile_x, tile_y in neighbor_tiles:
            targets.extend(self.engine.game_map.get_targets_at_location(tile_x, tile_y))
        if self.entity in targets:
            targets.remove(self.entity)
        super().__init__(entity, targets)
    
    def perform(self) -> bool:
        return super().perform()


class MouseMoveAction(Action):
    def __init__(self, entity: Actor, position: Tuple[int, int]):
        self.x = position[0]
        self.y = position[1]
        super().__init__(entity)
    
    @property
    def position(self):
        return self.x, self.y
    
    def perform(self) -> bool:
        self.engine.mouse_location = self.position
        return False
