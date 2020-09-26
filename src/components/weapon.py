from __future__ import annotations

from typing import TYPE_CHECKING

from components.base import BaseComponent

if TYPE_CHECKING:
    from components.broadsides import Broadsides


class Weapon(BaseComponent):
    parent: Broadsides
    
    def __init__(self, parent, hp: int, defense: int, dist: int, power: int,
                 cooldown: int, name: str = "weapon", can_hit: dict = "body"):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.range = dist
        self.power = power
        self.name = name
        self.can_hit = can_hit
        self.cooldown = 0
        self.cooldown_max = cooldown
        self.parent = parent
    
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0:
            self.destroy()
    
    def destroy(self):
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
