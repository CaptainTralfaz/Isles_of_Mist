from __future__ import annotations

from random import randint, choice
from typing import TYPE_CHECKING, Optional, List, Tuple

from components.cargo import Item
from constants import colors, move_elevations
from custom_exceptions import Impossible
from utilities import choice_from_dict, get_cone_target_hexes_at_location

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
                        and not (x, y) == self.engine.game_map.port) \
                       or ((x, y) == self.engine.game_map.port and self.entity == self.engine.player)
            if can_move:
                self.entity.move()
                if (x, y) == self.engine.game_map.port and self.entity is self.engine.player:
                    self.engine.message_log.add_message(f"Welcome to Port!", colors['cyan'])
                    if self.entity.sails.raised:
                        self.entity.sails.adjust()
                        return True
                color = colors['pink'] if self.entity == self.engine.player else colors['mountain']
                if self.entity.fighter.name == "hull":
                    if self.entity.parent.game_map.terrain[x][y].decoration:
                        decoration = self.entity.parent.game_map.terrain[x][y].decoration
                        if decoration in ['rocks']:
                            self.entity.parent.engine.message_log.add_message(
                                f"{self.entity.name} takes 2 hull damage while trying to dodge rocks", color)
                            self.entity.fighter.take_damage(2)
                        elif decoration in ['coral']:
                            self.entity.parent.engine.message_log.add_message(
                                f"{self.entity.name} takes 1 hull damage from scraping coral", color)
                            self.entity.fighter.take_damage(1)
                if not self.entity.flying and self.entity.parent.game_map.terrain[x][y].decoration:
                    if self.entity.parent.game_map.terrain[x][y].decoration in ['mines']:
                        damage = randint(2, 5)
                        if (self.entity.x, self.entity.y) in self.engine.player.view.fov:
                            self.entity.parent.engine.message_log.add_message(
                                f"Mines explode!", colors['red'])
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
                    self.engine.message_log.add_message("Blocked", colors['gray'])
                    self.entity.sails.adjust()
                else:
                    raise Impossible("Blocked")
            return False
        # player out of bounds
        elif self.entity == self.engine.player:
            if self.entity.sails and self.entity.sails.hp > 0 and self.entity.sails.raised:
                self.engine.message_log.add_message("No Navigational Charts to leave area", colors['gray'])
                self.entity.sails.adjust()
            else:
                raise Impossible("No Navigational Charts to leave area")


class RotateAction(Action):
    def __init__(self, entity, direction):
        super().__init__(entity)
        self.direction = direction
    
    def perform(self) -> bool:
        self.entity.rotate(self.direction)
        return True


class ShipAction(Action):
    def __init__(self, entity, event):
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event == "sails":
            return SailAction(self.entity).perform()
        raise Impossible(f"{self.event} not implemented...")


class SailAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.sails.hp > 0:
            self.entity.sails.adjust()
            return True
        else:
            raise Impossible("Sails are too damaged to raise")


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
        if self.direction in ["port", "starboard"]:
            return BroadsideAction(self.entity, self.direction).perform()
        if self.direction in ["fore"]:
            return ArrowAction(self.entity, self.direction).perform()
        if self.direction in ["aft"]:
            return MineAction(self.entity).perform()
        return False


class SplitDamageAction(Action):
    def __init__(self, entity: Actor, targets: List[Actor], damage, direction):
        super().__init__(entity)
        self.targets = targets
        self.damage = damage
        self.direction = direction
    
    def perform(self) -> bool:
        for target in self.targets:
            damage = self.damage - target.fighter.defense
            
            attack_desc = f"{self.entity.name.capitalize()} shoots {target.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} " +
                                                    f"{target.fighter.name} damage",
                                                    colors['mountain'])
                target.fighter.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage",
                                                    colors['mountain'])
        if self.direction == "port":
            for weapon in [w for w in self.entity.broadsides.port if w.cooldown == 0]:
                weapon.cooldown = weapon.cooldown_max
        elif self.direction == "starboard":
            for weapon in [w for w in self.entity.broadsides.starboard if w.cooldown == 0]:
                weapon.cooldown = weapon.cooldown_max
        return True


class BroadsideAction(SplitDamageAction):
    def __init__(self, entity, direction):
        self.entity = entity
        
        distance = self.entity.broadsides.get_active_range(direction)
        if distance:
            damage = self.entity.broadsides.get_active_power(direction)
        else:
            raise Impossible(f"No active weapons to {direction}")
        targets = []
        hexes = get_cone_target_hexes_at_location(entity, direction, distance)
        for x, y in hexes:
            if (x, y) in entity.view.fov:
                targets.extend(self.engine.game_map.get_targets_at_location(x, y))
        if self.entity in targets:
            targets.remove(self.entity)
        if len(targets) < 1:
            raise Impossible(f"No targets to {direction}")
        damage = damage // len(targets)
        super().__init__(entity, targets, damage, direction)

    def perform(self) -> bool:
        return super().perform()


class ArrowAction(SplitDamageAction):
    def __init__(self, entity: Actor, direction):
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
        
        if len(targets) < 1:
            raise Impossible(f"No adjacent targets")
        damage = (self.entity.crew.count // 3) // len(targets)
        super().__init__(entity, targets, damage, direction)
    
    def perform(self) -> bool:
        return super().perform()


class AutoAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        # make a decision on automatic action
        salvage = self.engine.game_map.get_items_at_location(self.entity.x, self.entity.y)
        if len(salvage) > 0:
            return SalvageAction(self.entity, salvage).perform()
        return WaitAction(self.entity).perform()


class SalvageAction(Action):
    def __init__(self, entity, salvage):
        super().__init__(entity)
        self.salvage = salvage
    
    def perform(self) -> bool:
        for salvage in self.salvage:
            self.engine.message_log.add_message(f"You salvage {salvage.name}!", colors['beach'])
            self.entity.cargo.add_items_to_manifest(salvage.cargo.manifest)
            
            for item in salvage.cargo.manifest.keys():
                self.engine.message_log.add_message(f"salvaged {salvage.cargo.manifest[item]} {item}",
                                                    colors['beach'])
            # remove salvage from entities list
            self.engine.game_map.entities.remove(salvage)
        return True
        # if item.name in self.manifest.keys():
        #     self.manifest[item.name] += item.quantity
        # else:
        #     self.manifest[item.name] = item.quantity


class RepairAction(Action):
    def __init__(self, entity, event):
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event == "crew":
            return HireCrewAction(self.entity).perform()
        if self.event == "sails":
            return RepairSailsAction(self.entity).perform()
        if self.event == "shipyard":
            return RepairHullAction(self.entity).perform()
        if self.event == "weapons":
            return RepairWeaponsAction(self.entity).perform()


class PortAction(Action):
    def __init__(self, entity, event):
        self.event = event
        super().__init__(entity)

    def perform(self) -> bool:
        if self.event == "merchant":
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == "barracks":
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == "shipyard":
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == "tavern":
            raise Impossible(f"{self.event} action yet implemented")
        return True


class HireCrewAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.crew.count < self.entity.crew.max_count:
            self.entity.crew.hire(1)
            self.engine.time.roll_hrs(1)
            self.engine.message_log.add_message(f"Hired 1 Sailor (an hour passes)")
            return True
        raise Impossible(f"Crew is full!", colors['gray'])


class RepairSailsAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.sails.hp < self.entity.sails.max_hp:
            self.entity.sails.repair(1)
            self.engine.time.roll_hrs(1)
            self.engine.message_log.add_message(f"Repaired 1 Sail (an hour passes)")
            return True
        raise Impossible(f"Sails are already repaired", colors['gray'])


class RepairWeaponsAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        damaged = self.entity.broadsides.get_damaged_weapons()
        hrs = 0
        if damaged:
            for weapon in damaged:
                weapon.repair(1)
                hrs += 1
        if hrs:
            hours = "hours" if hrs > 1 else "hour"
            passes = "pass" if hrs > 1 else "passes"
            self.engine.time.roll_hrs(hrs)
            self.engine.message_log.add_message(f"Repaired {hrs} Weapons damage ({hrs} {hours} {passes})")
            return True
        raise Impossible(f"Weapons are already fully repaired", colors['gray'])


class RepairHullAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.fighter.hp < self.entity.fighter.max_hp:
            self.entity.fighter.repair(1)
            self.engine.time.roll_hrs(2)
            self.engine.message_log.add_message(f"Repaired 1 Hull Point (2 hours pass)")
            return True
        raise Impossible(f"Hull is already repaired", colors['gray'])


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
        
        if "sail" in self.entity.fighter.can_hit.keys() and ((not self.target.sails)
                                                             or self.target.sails.hp == 0
                                                             or (not self.target.sails.raised)):
            self.entity.fighter.can_hit["sail"] = 0
        
        if "weapon" in self.entity.fighter.can_hit.keys() and ((not self.target.broadsides)
                                                               or (len(self.target.broadsides.port)
                                                                   + len(self.target.broadsides.starboard) < 1)):
            self.entity.fighter.can_hit["weapon"] = 0
        
        gets_hit = choice_from_dict(self.entity.fighter.can_hit)
        
        if gets_hit == "hull":
            damage = self.entity.fighter.power - self.target.fighter.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.fighter.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} damage", colors['pink'])
                self.target.fighter.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors['pink'])
        elif gets_hit == "sail":
            damage = self.entity.fighter.power - self.target.sails.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.sails.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} damage", colors['pink'])
                self.target.sails.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors['pink'])
        elif gets_hit == "crew":
            damage = self.entity.fighter.power - self.target.crew.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.crew.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} and kills {damage} members", colors['pink'])
                self.target.crew.count -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors['pink'])
        elif gets_hit == "weapon":
            weapon, location = self.target.broadsides.pick_weapon()
            damage = self.entity.fighter.power - weapon.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {weapon.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} damage", colors['pink'])
                destroy = weapon.hp - damage
                if destroy <= 0:
                    self.engine.message_log.add_message(
                        f"{location.capitalize()} {weapon.name.capitalize()} was destroyed!", colors['orange'])
                weapon.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors['pink'])
        return True


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
