from __future__ import annotations

from random import choice
from typing import List, Tuple, Dict, Optional
from typing import TYPE_CHECKING

from components.base import BaseComponent
from components.weapon import Weapon
from constants.enums import Location
from constants.stats import item_stats
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity

max_slots = 4


class Broadsides(BaseComponent):
    parent: Entity
    
    def __init__(self, slot_count: int,
                 port: List[Weapon],
                 starboard: List[Weapon],
                 storage: List[Weapon]) -> None:
        self.slot_count = slot_count
        self.port = port
        self.starboard = starboard
        self.storage = storage
        for location, weapon in self.all_weapons:
            weapon.parent = self
        
        self.selected = 0
        self.sell_list = []
        self.buy_list = []
    
    def to_json(self) -> Dict:
        return {
            'slot_count': self.slot_count,
            'port': [weapon.to_json() for weapon in self.port],
            'starboard': [weapon.to_json() for weapon in self.starboard],
            'storage': [weapon.to_json() for weapon in self.storage]
        }
    
    @staticmethod
    def from_json(json_data):
        slot_count = json_data.get('slot_count')
        port_data = json_data.get('port')
        starboard_data = json_data.get('starboard')
        storage_data = json_data.get('storage')
        port = []
        for weapon in port_data:
            port.append(Weapon.from_json(weapon))
        starboard = []
        for weapon in starboard_data:
            starboard.append(Weapon.from_json(weapon))
        storage = []
        for weapon in storage_data:
            storage.append(Weapon.from_json(weapon))
        broadsides = Broadsides(slot_count=slot_count, port=port, starboard=starboard, storage=storage)
        return broadsides
    
    @property
    def weight(self) -> int:
        """
        Determines total weight of weapons
        :return: total weight of weapons
        """
        weight = 0
        for location, weapon in self.all_weapons:
            weight += item_stats[weapon.name.lower()]['weight']
        return weight
    
    @property
    def volume(self) -> int:
        """
        Determines total volume of weapons
        :return: total volume of weapons
        """
        weight = 0
        for location, weapon in self.all_weapons:
            weight += item_stats[weapon.name.lower()]['volume']
        return weight
    
    @property
    def all_weapons(self) -> List[Tuple[Location, Weapon]]:
        weapon_list = []
        for weapon in self.port:
            weapon_list.append((Location.PORT, weapon))
        for weapon in self.starboard:
            weapon_list.append((Location.STARBOARD, weapon))
        for weapon in self.storage:
            weapon_list.append((Location.STORAGE, weapon))
        return weapon_list
    
    def attach(self, location: Location, weapon: Weapon) -> None:
        """
        Attaches a weapon to port or starboard broadside. Cooldown not toggled on new game
        :param location: Enum port or starboard
        :param weapon: instance of Weapon to attach
        :return: None
        """
        if location == Location.PORT:
            if len(self.port) < self.slot_count:
                self.port.append(weapon)
                weapon.cooldown = weapon.cooldown_max
                weapon.parent = self
        elif location == Location.STARBOARD:
            if len(self.starboard) < self.slot_count:
                self.starboard.append(weapon)
                weapon.cooldown = weapon.cooldown_max
                weapon.parent = self
    
    def detach(self, weapon: Weapon) -> None:
        """
        Removes a weapon from broadside, puts weapon in storage
        :param weapon: Weapon instance
        :return: None
        """
        if weapon in self.port:
            self.port.remove(weapon)
            self.storage.append(weapon)
        elif weapon in self.starboard:
            self.starboard.remove(weapon)
            self.storage.append(weapon)
    
    def get_active_weapons(self, location: str) -> List[Weapon]:
        """
        Generates a list of Weapons that are not on cooldown
        :param location: Enum port or starboard
        :return: List of Weapons
        """
        if location == Location.PORT:
            return [weapon for weapon in self.port if weapon.cooldown == 0]
        else:
            return [weapon for weapon in self.starboard if weapon.cooldown == 0]
    
    def get_active_power(self, location: Location) -> Optional[int]:
        """
        Totals power of all Weapons not on cooldown
        :param location: Enum port or starboard
        :return:
        """
        if location == Location.PORT:
            power = [weapon.power for weapon in self.port if weapon.cooldown == 0]
        else:
            power = [weapon.power for weapon in self.starboard if weapon.cooldown == 0]
        if len(power) > 0:
            return sum(power)
        else:
            return None
    
    def get_active_weapon_ammo_types(self, location: Location) -> Dict[str, int]:
        """
        creates a dictionary of ammo types mapped to a count of active Weapons using that ammo type
        :param location: Enum port or starboard
        :return: dict of ammo types to count
        """
        if location == Location.PORT:
            ammo_list = [weapon.ammo for weapon in self.port if weapon.cooldown == 0]
        else:
            ammo_list = [weapon.ammo for weapon in self.starboard if weapon.cooldown == 0]
        ammo = {}
        for ammo_type in ammo_list:
            if ammo_type in ammo.keys():
                ammo[ammo_type] += 1
            else:
                ammo[ammo_type] = 1
        return ammo
    
    def get_attached_weapon_ammo_types(self) -> List[str]:
        """
        creates a list of ammo types for attached weapons
        :return: list of strings of ammo names
        """
        ammo_list = []
        for weapon in self.port:
            if weapon.ammo not in ammo_list:
                ammo_list.append(weapon.ammo)
        for weapon in self.starboard:
            if weapon.ammo not in ammo_list:
                ammo_list.append(weapon.ammo)
        return ammo_list
    
    def get_damaged_weapons(self) -> List[Weapon]:
        """
        creates a list of Weapons that are damaged
        :return: list of Weapons
        """
        damaged = [weapon for location, weapon in self.all_weapons if weapon.hp < weapon.max_hp]
        return damaged
    
    def get_active_range(self, location: Location) -> Optional[int]:
        """
        creates a list of maximum active weapon ranges
        :param location: Enum port or starboard
        :return: int range or None
        """
        if location == Location.PORT:
            ranges = [weapon.range for weapon in self.port if weapon.cooldown == 0]
        else:
            ranges = [weapon.range for weapon in self.starboard if weapon.cooldown == 0]
        if len(ranges) > 0:
            return max(ranges)
        else:
            return None
    
    def tick_cooldown(self) -> None:
        """
        reduce cooldown turn by 1 for every attached weapon on cooldown
        :return: None
        """
        for weapon in [w for w in self.port if w.cooldown > 0]:
            weapon.cooldown -= 1
        for weapon in [w for w in self.starboard if w.cooldown > 0]:
            weapon.cooldown -= 1
    
    def upgrade(self) -> None:
        """
        Increase the number of weapons that can be attached per side
        :return: None
        """
        if self.slot_count + 1 > max_slots:
            raise Impossible("Weapon slots already at maximum")
        self.slot_count += 1
        self.parent.game_map.engine.message_log.add_message(
            f"Upgraded maximum number of weapons per side to {self.slot_count}", text_color='cyan')
    
    def pick_weapon(self) -> (Weapon, Location):
        """
        pick a random attached weapon
        :return: Weapon instance and Location it is attached
        """
        side = []
        if len(self.port) > 0:
            side.append(Location.PORT)
        if len(self.starboard) > 0:
            side.append(Location.STARBOARD)
        pick = choice(side)
        if pick == Location.PORT:
            weapon = choice(self.port)
            return weapon, pick
        else:
            weapon = choice(self.starboard)
            return weapon, pick
    
    def destroy(self, weapon: Weapon) -> None:
        """
        Destroy a Weapon instance (removes it from appropriate list)
        :param weapon: Weapon to destroy
        :return: None
        """
        if weapon in self.storage:
            self.storage.remove(weapon)
        elif weapon in self.port:
            self.port.remove(weapon)
        elif weapon in self.starboard:
            self.starboard.remove(weapon)
