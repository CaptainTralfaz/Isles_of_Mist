from __future__ import annotations

from typing import TYPE_CHECKING

from components.base import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class Sails(BaseComponent):
    parent: Actor
    
    def __init__(self, hp: int, defense: int, raised: bool = True, name: str = "sail"):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.raised = raised
        self.name = name
    
    def to_json(self):
        return {
            'max_hp': self.max_hp,
            '_hp': self._hp,
            'defense': self.defense,
            'raised': self.raised
        }
    
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0:
            self.destroy()
    
    def repair(self, amount: int) -> int:
        new_sail_value = self.hp + amount
        if new_sail_value > self.max_hp:
            new_sail_value = self.max_hp
        amount_repaired = new_sail_value - self.hp
        self.hp = new_sail_value
        return amount_repaired
    
    def destroy(self):
        self.raised = False
        self.engine.message_log.add_message(f"Sails have been destroyed!", text_color='aqua')
    
    def adjust(self):
        if self.raised:
            self.raised = False
            self.engine.message_log.add_message(f"Sails trimmed", text_color='aqua')
        else:
            self.raised = True
            self.engine.message_log.add_message(f"Sails raised", text_color='aqua')
