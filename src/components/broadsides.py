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
                        weapon=Weapon(parent=self, hp=3, defense=0, dist=3, power=4, cooldown=4, name="Ballista"))
        else:
            for weapon in port:
                self.attach(location="port", weapon=weapon)
        if starboard is None:
            self.starboard = []
            self.attach(location="starboard",
                        weapon=Weapon(parent=self, hp=3, defense=0, dist=3, power=4, cooldown=4, name="Ballista"))
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
