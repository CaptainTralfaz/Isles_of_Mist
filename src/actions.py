from __future__ import annotations

from random import randint, choice
from typing import TYPE_CHECKING, Optional, List, Tuple, Dict

from constants import colors, move_elevations, Location
from custom_exceptions import Impossible
from game_states import GameStates
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


class ExitMenuAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.is_alive:
            self.engine.game_state = GameStates.ACTION
            self.entity.cargo.selected = 0
            self.entity.crew.selected = 0
            self.entity.broadsides.selected = 0
        else:
            self.engine.game_state = GameStates.PLAYER_DEAD
        return False


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
            # TODO currently no decorations on land (except port)
            # use this for when a point of interest is added to a coastline space,
            #  examples: hermit hut, fisherman village, "X" marks the spot
            # event = (self.entity == self.engine.player and
            #          self.entity.game_map.terrain[x][y].decoration is not None)
            can_move = (self.entity.game_map.can_move_to(x, y, self.entity.elevations)
                        and not (x, y) == self.engine.game_map.port) \
                       or ((x, y) == self.engine.game_map.port and self.entity == self.engine.player)
            if can_move:
                self.entity.move()
                if (x, y) == self.engine.game_map.port and self.entity is self.engine.player:
                    self.engine.message_log.add_message(f"Welcome to Port!", colors['cyan'])
                    if self.entity.sails.raised:
                        self.entity.sails.adjust()
                # damage from terrain decorations
                elif self.entity.game_map.terrain[x][y].decoration is not None:
                    self.entity.game_map.decoration_damage(x=x, y=y, entity=self.entity,
                                                           conditions=self.engine.weather.conditions)
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
    def __init__(self, entity, event, status):
        self.event = event
        self.status = status
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event == "sails":
            return SailAction(self.entity).perform()
        else:
            return ConfigureAction(self.entity, self.event, self.status).perform()


class ConfigureAction(Action):
    def __init__(self, entity: Actor, event: str, state: GameStates) -> None:
        self.event = event
        self.state = state
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event in ["up", "sails"]:
            return False
        elif self.event in ["down", "weapons"]:
            if self.state == GameStates.WEAPON_CONFIG:
                return ExitMenuAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.WEAPON_CONFIG
            return False
        elif self.event in ["left", "crew"]:
            if self.state == GameStates.CREW_CONFIG:
                return ExitMenuAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.CREW_CONFIG
            return False
        elif self.event in ["right", "cargo"]:
            if self.state == GameStates.CARGO_CONFIG:
                return ExitMenuAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.CARGO_CONFIG
            return False
        raise Impossible(f"bad state {self.event}   wtf...")


class ChangeSelectionAction(Action):
    def __init__(self, entity, event, state):
        self.event = event
        self.state = state
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.state == GameStates.WEAPON_CONFIG:
            component = self.entity.broadsides
            length = len(self.entity.broadsides.all_weapons) - 1
        elif self.state == GameStates.CARGO_CONFIG:
            component = self.entity.cargo
            length = len(self.entity.cargo.manifest.keys()) - 1
        elif self.state == GameStates.CREW_CONFIG:
            component = self.entity.crew
            length = len(self.entity.crew.roster) - 1
        else:
            raise Impossible("Bad State")
        
        if self.event == "up":
            component.selected -= 1
            if component.selected < 0:
                component.selected = length
        if self.event == "down":
            component.selected += 1
            if component.selected > length:
                component.selected = 0
        return False


class AssignCrewAction(Action):
    def __init__(self, entity, event):
        super().__init__(entity)
        self.event = event
    
    def perform(self) -> bool:
        if not self.entity.is_alive:
            raise Impossible("Can't assign crew when dead")
        if self.entity.crew.assignments[self.event] == self.entity.crew.roster[self.entity.crew.selected]:
            self.entity.crew.assignments[self.event] = None
            self.engine.message_log.add_message(f"assigning nobody to '{self.event}' key")
            return False
        else:
            self.entity.crew.assignments[self.event] = self.entity.crew.roster[self.entity.crew.selected]
            self.engine.message_log.add_message(f"assigning {self.entity.crew.roster[self.entity.crew.selected].name}"
                                                f" to '{self.event}' key")
            self.engine.game_state = GameStates.ACTION
            return True


class AssignWeaponAction(Action):
    def __init__(self, entity, event, state):
        super().__init__(entity)
        self.event = event
        self.state = state
    
    def perform(self) -> bool:
        if not self.entity.is_alive:
            raise Impossible("Can't assign weapons when dead")
        if self.event in ["up", "down"]:
            return ChangeSelectionAction(self.entity, self.event, self.state).perform()
        
        location, weapon = self.entity.broadsides.all_weapons[self.entity.broadsides.selected]
        if location in ["storage"]:
            if self.event == "left" and len(self.entity.broadsides.port) < self.entity.broadsides.slot_count:
                self.entity.broadsides.attach(location=Location.PORT, weapon=weapon)
                self.entity.broadsides.storage.remove(weapon)
                self.engine.message_log.add_message(f"Readied {weapon.name.capitalize()} to Port ")
                self.engine.game_state = GameStates.ACTION
                return True
            elif self.event == "right" and len(self.entity.broadsides.starboard) < self.entity.broadsides.slot_count:
                self.entity.broadsides.attach(location=Location.STARBOARD, weapon=weapon)
                self.entity.broadsides.storage.remove(weapon)
                self.engine.message_log.add_message(f"Readied {weapon.name.capitalize()} to Starboard ")
                self.engine.game_state = GameStates.ACTION
                return True
        elif location in [Location.PORT]:
            if self.event == "left":
                self.entity.broadsides.detach(weapon)
                self.engine.message_log.add_message(f"Removed {weapon.name.capitalize()} from Port ")
                self.engine.game_state = GameStates.ACTION
                return True
        elif location in [Location.STARBOARD]:
            if self.event == "right":
                self.entity.broadsides.detach(weapon)
                self.engine.message_log.add_message(f"Removed {weapon.name.capitalize()} from Starboard ")
                self.engine.game_state = GameStates.ACTION
                return True
        return False


class SelectedAction(Action):
    def __init__(self, entity, event, state):
        self.event = event
        self.state = state
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.state == GameStates.CREW_CONFIG:
            return AssignCrewAction(self.entity, self.event).perform()
        if self.state == GameStates.WEAPON_CONFIG:
            return AssignWeaponAction(self.entity, self.event, self.state).perform()
        print(f"moving selection {self.event}")
        return False


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
        if not self.entity.cargo.item_type_in_manifest('mines'):
            raise Impossible("No mines in inventory!")
        self.engine.game_map.terrain[self.entity.x][self.entity.y].decoration = "minefield"
        self.entity.cargo.remove_items_from_manifest({'mines': 1})
        self.engine.message_log.add_message("Mines placed")
        return True


class AttackAction(Action):
    def __init__(self, entity, direction):
        super().__init__(entity)
        self.direction = direction
    
    def perform(self) -> bool:
        if self.direction in [Location.PORT, Location.STARBOARD]:
            return BroadsideAction(self.entity, self.direction).perform()
        if self.direction in [Location.FORE]:
            return ArrowAction(self.entity, self.direction).perform()
        if self.direction in [Location.AFT]:
            return MineAction(self.entity).perform()
        return False


class SplitDamageAction(Action):
    def __init__(self, entity: Actor,
                 targets: List[Actor],
                 damage: int,
                 direction: Location,
                 ammo: Dict[str, int]):
        super().__init__(entity)
        self.targets = targets
        self.damage = damage
        self.direction = direction
        self.ammo = ammo
    
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
        if self.direction == Location.PORT:
            for weapon in [w for w in self.entity.broadsides.port if w.cooldown == 0]:
                weapon.cooldown = weapon.cooldown_max
        elif self.direction == Location.STARBOARD:
            for weapon in [w for w in self.entity.broadsides.starboard if w.cooldown == 0]:
                weapon.cooldown = weapon.cooldown_max
        self.entity.cargo.remove_items_from_manifest(self.ammo)
        return True


class BroadsideAction(SplitDamageAction):
    def __init__(self, entity, direction: Location):
        self.entity = entity
        
        distance = self.entity.broadsides.get_active_range(direction)
        if distance:
            damage = self.entity.broadsides.get_active_power(direction)
        else:
            raise Impossible(f"No active weapons to {direction.name.lower().capitalize()}")
        ammo = self.entity.broadsides.get_active_weapon_ammo_types(direction)
        enough_ammo = True
        for ammo_type in ammo.keys():
            if ammo_type not in self.entity.cargo.manifest.keys():
                enough_ammo = False
            elif self.entity.cargo.manifest[ammo_type] - ammo[ammo_type] < 0:
                enough_ammo = False
        if not enough_ammo:
            raise Impossible(f"Not enough ammo to fire {direction.name.lower().capitalize()} Broadsides")
        targets = []
        hexes = get_cone_target_hexes_at_location(entity.x, entity.y, entity.facing, direction, distance)
        for x, y in hexes:
            if (x, y) in entity.view.fov:
                targets.extend(self.engine.game_map.get_targets_at_location(x, y))
        if self.entity in targets:
            targets.remove(self.entity)
        if len(targets) < 1:
            raise Impossible(f"No targets to {direction.name.lower().capitalize()}")
        
        damage = damage // len(targets)
        super().__init__(entity, targets, damage, direction, ammo)
    
    def perform(self) -> bool:
        return super().perform()


class ArrowAction(SplitDamageAction):
    def __init__(self, entity: Actor, direction: Location):
        self.entity = entity
        ammo = {'arrows': self.entity.crew.count // 4}
        enough_ammo = True
        for ammo_type in ammo.keys():
            if ammo_type not in self.entity.cargo.manifest.keys():
                enough_ammo = False
            elif self.entity.cargo.manifest[ammo_type] - ammo[ammo_type] < 0:
                enough_ammo = False
        if not enough_ammo:
            raise Impossible(f"Not enough arrows!")
        
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
        damage = (self.entity.crew.count // 4) // len(targets)
        super().__init__(entity, targets, damage, direction, ammo)
    
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
            self.engine.message_log.add_message(f"You salvage {salvage.name}!", colors['orange'])
            self.entity.cargo.add_items_to_manifest(salvage.cargo.manifest)
            self.engine.game_map.entities.remove(salvage)
        return True


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
        if self.event == "engineer":
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
                self.target.crew.take_damage(damage)
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
                        f"{location.name.capitalize()} {weapon.name.capitalize()} was destroyed!", colors['orange'])
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
