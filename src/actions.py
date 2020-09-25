from __future__ import annotations

from random import randint, choice
from typing import TYPE_CHECKING, Optional, List, Tuple

from constants import colors, move_elevations
from custom_exceptions import Impossible
from utilities import choice_from_dict

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
        if self.entity.sails and self.entity.sails.raised:
            self.engine.message_log.add_message(f"{self.entity.name} coasts...")
        else:
            self.engine.message_log.add_message(f"{self.entity.name} waits...")
        return True


class MovementAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        x, y = self.entity.get_next_hex()
        if self.entity.game_map.in_bounds(x, y):
            can_move = (self.entity.game_map.game_map.can_move_to(x, y, self.entity.elevations)
                        and (x, y) is not self.engine.game_map.port) \
                       or ((x, y) == self.engine.game_map.port and self.entity == self.engine.player)
            if can_move:
                self.entity.move()
                if (x, y) == self.engine.game_map.port and self.entity is self.engine.player:
                    if self.entity.sails.raised:
                        self.engine.message_log.add_message("You sail into Port")
                        self.entity.sails.adjust(False)
                        return True
                color = colors["enemy_atk"] if self.entity == self.engine.player else colors["player_atk"]
                if self.entity.fighter.name == "hull":
                    if self.entity.parent.game_map.terrain[x][y].decoration:
                        decoration = self.entity.parent.game_map.terrain[x][y].decoration
                        if decoration in ["rocks"]:
                            self.entity.parent.engine.message_log.add_message(
                                f"{self.entity.name} takes 2 hull damage while trying to dodge rocks", color)
                            self.entity.fighter.take_damage(2)
                        elif decoration in ["coral"]:
                            self.entity.parent.engine.message_log.add_message(
                                f"{self.entity.name} takes 1 hull damage from scraping coral", color)
                            self.entity.fighter.take_damage(1)
                if not self.entity.flying and self.entity.parent.game_map.terrain[x][y].decoration:
                    if self.entity.parent.game_map.terrain[x][y].decoration in ["mines"]:
                        damage = randint(2, 5)
                        if (self.entity.x, self.entity.y) in self.engine.player.view.fov:
                            self.entity.parent.engine.message_log.add_message(
                                f"Mines explode!", colors['player_die'])
                            self.entity.parent.engine.message_log.add_message(
                                f"{self.entity.name} takes {damage} {self.entity.fighter.name} damage!", color)
                        self.entity.fighter.take_damage(damage)
                        if damage > 3:
                            if (self.entity.x, self.entity.y) in self.engine.player.view.fov:
                                self.entity.parent.engine.message_log.add_message(
                                    f"Minefield has been cleared")
                            self.entity.parent.game_map.terrain[x][y].decoration = None
                return True
            # player can't move here
            elif self.entity == self.engine.player:
                if self.entity.sails and self.entity.sails.hp > 0 and self.entity.sails.raised:
                    self.engine.message_log.add_message("Blocked", colors['impossible'])
                    self.entity.sails.adjust(False)
                else:
                    raise Impossible("Blocked")
            return False
        # player out of bounds
        elif self.entity == self.engine.player:
            if self.entity.sails and self.entity.sails.hp > 0 and self.entity.sails.raised:
                self.engine.message_log.add_message("No Navigational Charts to leave area", colors['impossible'])
                self.entity.sails.adjust(False)
            else:
                raise Impossible("No Navigational Charts to leave area")


class RotateAction(Action):
    def __init__(self, entity, direction):
        super().__init__(entity)
        self.direction = direction
    
    def perform(self) -> bool:
        self.entity.rotate(self.direction)
        return True


class SailAction(Action):
    def __init__(self, entity, sail):
        super().__init__(entity)
        self.sail = sail
    
    def perform(self) -> bool:
        if self.entity.sails.hp > 0:
            self.entity.sails.adjust(self.sail)
            return True
        else:
            raise Impossible("No Sails")


class MineAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        self.engine.game_map.terrain[self.entity.x][self.entity.y].decoration = "mines"
        self.engine.message_log.add_message(f"Mines placed")
        return True


class AttackAction(Action):
    def __init__(self, entity, direction):
        super().__init__(entity)
        self.direction = direction
    
    def perform(self) -> bool:
        if self.entity == self.engine.player and (self.entity.x, self.entity.y) == self.engine.game_map.port:
            raise Impossible("Can't attack while in town")
        if self.direction in ["port", "starboard"]:
            raise Impossible("Not yet Implemented")
        if self.direction in ["fore"]:
            return ArrowAction(self.entity).perform()
        if self.direction in ["aft"]:
            return MineAction(self.entity).perform()
        return False


class AutoAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        # make a decision on automatic action
        return WaitAction(self.entity).perform()


class WanderAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        decision = randint(-1, 1)
        x, y = self.entity.get_next_hex()
        if decision == 0 \
                and self.engine.game_map.in_bounds(x, y) \
                and self.engine.game_map.can_move_to(x, y, self.entity.elevations):
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
        
        if "sail" in self.entity.fighter.can_hit.keys() and (self.target.sails.hp == 0
                                                             or not self.target.sails.raised):
            self.entity.fighter.can_hit["sail"] = 0
        
        gets_hit = choice_from_dict(self.entity.fighter.can_hit)
        
        if gets_hit == "hull":
            damage = self.entity.fighter.power - self.target.fighter.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.fighter.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} damage", colors["enemy_atk"])
                self.target.fighter.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors["enemy_atk"])
        elif gets_hit == "sail":
            damage = self.entity.fighter.power - self.target.sails.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.sails.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} damage", colors["enemy_atk"])
                self.target.sails.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors["enemy_atk"])
        elif gets_hit == "crew":
            damage = self.entity.fighter.power - self.target.crew.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.crew.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} and kills {damage} members", colors["enemy_atk"])
                self.target.crew.count -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors["enemy_atk"])
        return True


class SplitDamageAction(Action):
    def __init__(self, entity: Actor, targets: List[Actor]):
        super().__init__(entity)
        self.targets = targets
    
    def perform(self) -> bool:
        if len(self.targets) > 0:
            split_damage = (self.entity.crew.count // 3) // len(self.targets)
            for target in self.targets:
                damage = split_damage - target.fighter.defense
                
                attack_desc = f"{self.entity.name.capitalize()} shoots {target.name}"
                if damage > 0:
                    self.engine.message_log.add_message(f"{attack_desc} for {damage} " +
                                                        f"{target.fighter.name} damage",
                                                        colors["player_atk"])
                    target.fighter.hp -= damage
                else:
                    self.engine.message_log.add_message(f"{attack_desc} but does no damage",
                                                        colors["player_atk"])
            return True
        raise Impossible("No Targets")


class ArrowAction(SplitDamageAction):
    def __init__(self, entity: Actor):
        self.entity = entity
        targets = []
        neighbor_tiles = self.engine.game_map.get_neighbors_at_elevations(self.entity.x,
                                                                          self.entity.y,
                                                                          elevations=move_elevations['all'])
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
