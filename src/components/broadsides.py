from random import choice
from typing import List, Tuple

from components.base import BaseComponent
from components.weapon import Weapon
from constants import colors, weapons
from custom_exceptions import Impossible
from entity import Actor

max_slots = 4


class Broadsides(BaseComponent):
    parent: Actor
    
    def __init__(self, slot_count: int,
                 port: List[str] = None,
                 starboard: List[str] = None,
                 storage: List[str] = None) -> None:
        self.slot_count = slot_count
        self.port = []
        self.starboard = []
        self.storage = []
        if port is not None:
            for weapon in port:
                self.attach(location="port", weapon=weapon)
        if starboard is not None:
            for weapon in starboard:
                self.attach(location="starboard", weapon=weapon)
        self.selected = 0
        if storage is not None:
            for weapon in storage:
                self.storage.append(self.make_weapon(name=weapon))
    
    @property
    def all_weapons(self) -> List[Tuple[str, Weapon]]:
        weapon_list = []
        for weapon in self.port:
            weapon_list.append(("port", weapon))
        for weapon in self.starboard:
            weapon_list.append(("starboard", weapon))
        for weapon in self.storage:
            weapon_list.append(("storage", weapon))
        return weapon_list
    
    def make_weapon(self, name: str):
        weapon = weapons[name]
        return Weapon(parent=self,
                      hp=weapon['hp'],
                      defense=weapon['defense'],
                      dist=weapon['range'],
                      power=weapon['power'],
                      cooldown=weapon['cooldown'],
                      name=name.capitalize(),
                      ammo=weapon['ammo'])
    
    def attach(self, location: str, weapon: str) -> None:
        if location == "port":
            if len(self.port) < self.slot_count:
                self.port.append(self.make_weapon(weapon))
        elif location == "starboard":
            if len(self.starboard) < self.slot_count:
                self.starboard.append(self.make_weapon(weapon))
            
    def detach(self, weapon: Weapon) -> None:
        if weapon in self.port:
            self.port.remove(weapon)
            self.storage.append(weapon)
        elif weapon in self.starboard:
            self.starboard.remove(weapon)
            self.storage.append(weapon)

    def get_active_weapons(self, location):
        if location == "port":
            return [weapon for weapon in self.port if weapon.cooldown == 0]
        else:
            return [weapon for weapon in self.starboard if weapon.cooldown == 0]
    
    def get_active_power(self, location):
        if location == "port":
            power = [weapon.power for weapon in self.port if weapon.cooldown == 0]
        else:
            power = [weapon.power for weapon in self.starboard if weapon.cooldown == 0]
        if len(power) > 0:
            return sum(power)
        else:
            return None
    
    def get_active_weapon_ammo_types(self, location):
        if location == "port":
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
    
    def get_attached_weapon_ammo_types(self):
        ammo_list = []
        for weapon in self.port:
            if weapon.ammo not in ammo_list:
                ammo_list.append(weapon.ammo)
        return ammo_list
    
    def get_damaged_weapons(self):
        damaged = [weapon for weapon in self.port if weapon.hp < weapon.max_hp]
        damaged.extend(weapon for weapon in self.starboard if weapon.hp < weapon.max_hp)
        return damaged
    
    def get_active_range(self, location):
        if location == "port":
            ranges = [weapon.range for weapon in self.port if weapon.cooldown == 0]
        else:
            ranges = [weapon.range for weapon in self.starboard if weapon.cooldown == 0]
        if len(ranges) > 0:
            return max(ranges)
        else:
            return None
    
    def tick_cooldown(self):
        for weapon in [w for w in self.port if w.cooldown > 0]:
            weapon.cooldown -= 1
        for weapon in [w for w in self.starboard if w.cooldown > 0]:
            weapon.cooldown -= 1
    
    def upgrade(self) -> None:
        if self.slot_count + 1 > max_slots:
            raise Impossible("Weapon slots already at maximum")
        self.slot_count += 1
        self.parent.game_map.engine.message_log.add_message(
            f"Upgraded maximum number of weapons per side to {self.slot_count}", text_color=colors['cyan'])
    
    def pick_weapon(self) -> (Weapon, str):
        side = []
        if len(self.port) > 0:
            side.append("port")
        if len(self.starboard) > 0:
            side.append("starboard")
        pick = choice(side)
        if pick == "port":
            return self.port[-1], pick
        else:
            return self.starboard[-1], pick
