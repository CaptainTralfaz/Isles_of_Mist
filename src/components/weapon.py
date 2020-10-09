from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from components.base import BaseComponent

if TYPE_CHECKING:
    from components.broadsides import Broadsides


class Weapon(BaseComponent):
    parent: Broadsides
    
    def __init__(self, parent, hp: int, defense: int, dist: int, power: int,  ammo: str,
                 cooldown: int = 0, name: str = "weapon", can_hit: dict = "body",
                 max_hp: int = None, cooldown_max: int = None, ) -> None:
        self.max_hp = hp if max_hp is None else max_hp
        self._hp = hp
        self.defense = defense
        self.range = dist
        self.power = power
        self.name = name
        self.can_hit = can_hit
        self.cooldown = cooldown
        self.cooldown_max = cooldown if cooldown_max is None else cooldown
        self.parent = parent
        self.ammo = ammo

    def to_json(self) -> Dict:
        return {
            'max_hp': self.max_hp,
            '_hp': self._hp,
            'defense': self.defense,
            'range': self.range,
            'power': self.power,
            'name': self.name,
            'can_hit': self.can_hit,
            'cooldown': self.cooldown,
            'cooldown_max': self.cooldown_max,
            'ammo': self.ammo
        }
    
    @staticmethod
    def from_json(json_data: Dict) -> Weapon:
        max_hp = json_data.get('max_hp')
        hp = json_data.get('_hp')
        defense = json_data.get('defense')
        distance = json_data.get('range')
        power = json_data.get('power')
        name = json_data.get('name')
        can_hit = json_data.get('can_hit')
        cooldown = json_data.get('cooldown')
        cooldown_max = json_data.get('cooldown_max')
        ammo = json_data.get('ammo')
        return Weapon(parent=None, hp=hp, defense=defense, dist=distance, power=power, max_hp=max_hp,
                      cooldown=cooldown, ammo=ammo, name=name, can_hit=can_hit, cooldown_max=cooldown_max)
            
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0:
            self.parent.destroy(self)
    
    def repair(self, amount: int) -> int:
        new_hull_value = self.hp + amount
        if new_hull_value > self.max_hp:
            new_hull_value = self.max_hp
        amount_repaired = new_hull_value - self.hp
        self.hp = new_hull_value
        return amount_repaired
    
    def take_damage(self, amount: int) -> None:
        self.hp -= amount
