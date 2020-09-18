from components.base import BaseComponent
from constants import colors
from entity import Actor


class Sails(BaseComponent):
    parent: Actor
    
    def __init__(self, hp: int, defense: int, raised: bool = True, name: str = "sail"):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.raised = raised
        self.name = name
    
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0:
            self.destroy()
    
    def destroy(self):
        self.raised = False
        self.engine.message_log.add_message(f"Sails have been destroyed!", colors["welcome_text"])
