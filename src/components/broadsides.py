from random import choice

from components.base import BaseComponent
from components.weapon import Weapon
from constants import colors
from custom_exceptions import Impossible
from entity import Actor

max_slots = 4


class Broadsides(BaseComponent):
    parent: Actor
    
    def __init__(self, slot_count: int, port: list = None, starboard: list = None):
        self.slot_count = slot_count
        if port is None:
            self.port = []
            self.attach(location="port",
                        weapon=Weapon(parent=self, hp=3, defense=2, dist=3, power=3, cooldown=4, name="Ballista"))
            # self.attach(location="port",
            #             weapon=Weapon(parent=self, hp=4, defense=3, dist=4, power=4, cooldown=5, name="Cannon"))
        else:
            for weapon in port:
                self.attach(location="port", weapon=weapon)
        if starboard is None:
            self.starboard = []
            self.attach(location="starboard",
                        weapon=Weapon(parent=self, hp=3, defense=2, dist=3, power=3, cooldown=4, name="Ballista"))
        else:
            for weapon in starboard:
                self.attach(location="starboard", weapon=weapon)
        
    def attach(self, location: str, weapon: Weapon) -> None:
        if location == "port":
            if len(self.port) < self.slot_count:
                self.port.append(weapon)
        elif location == "starboard":
            if len(self.starboard) < self.slot_count:
                self.starboard.append(weapon)
    
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

    def destroy(self, weapon: Weapon) -> None:
        # self.parent.game_map.engine.message_log.add_message(f"{weapon.name} is destroyed!", color=colors['orange'])
        if weapon in self.port:
            self.port.remove(weapon)
        elif weapon in self.starboard:
            self.starboard.remove(weapon)
    
    def upgrade(self) -> None:
        if self.slot_count + 1 > max_slots:
            raise Impossible("Weapon slots already at maximum")
        self.slot_count += 1
        # self.parent.game_map.engine.message_log.add_message(
        #     f"Upgraded maximum number of weapons per side to {self.slot_count}", text_color=colors['cyan'])
    
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
