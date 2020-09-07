from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, Optional, List

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
        print("{} waits...".format(self.entity.name))
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
        if decision in [-1, 1]:
            return RotateAction(self.entity, decision).perform()
        elif decision == 0:
            return MovementAction(self.entity).perform()
        else:
            return WaitAction(self.entity).perform()


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
            print(f"{attack_desc} for {damage} hit points.")
            self.target.fighter.hp -= damage
            print(f"{self.target.fighter.hp}/{self.target.fighter.max_hp}")
        
        else:
            print(f"{attack_desc} but does no damage.")
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
                    print(f"{attack_desc} for {damage} hit points.")
                    target.fighter.hp -= damage
                    print(f"{target.fighter.hp}/{target.fighter.max_hp}")
                
                else:
                    print(f"{attack_desc} but does no damage.")
            return True
        print("No Targets")
        return False


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
        print(f"length of targets list: {len(targets)}")
        super().__init__(entity, targets)
    
    def perform(self) -> bool:
        return super().perform()
