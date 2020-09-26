from components.base import BaseComponent
from components.cargo import Cargo
from constants import colors
from entity import Actor
from game_map import Elevation
from input_handlers import GameOverEventHandler
from render_functions import RenderOrder
from procgen import get_entity_manifest


class Fighter(BaseComponent):
    parent: Actor
    
    def __init__(self, hp: int, defense: int, power: int, name: str = "body", can_hit: dict = None):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power
        self.name = name
        if can_hit is None:
            self.can_hit = {"hull": 50, "sail": 20, "crew": 10, "weapon": 10, "cargo": 10}
        else:
            self.can_hit = can_hit
    
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()
    
    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            self.parent.icon = 'shipwreck'
            self.engine.event_handler = GameOverEventHandler(self.engine)
            death_message_color = colors['red']
        else:
            self.parent.cargo = Cargo(20, 20, get_entity_manifest(self.parent.name))
            death_message = f"{self.parent.name} is dead!"
            if self.game_map.terrain[self.parent.x][self.parent.y].elevation < Elevation.BEACH:
                self.parent.icon = "carcass"
            else:
                self.parent.icon = None
            death_message_color = colors['orange']
            self.parent.view = None
        
        if self.parent.sprite:
            self.parent.sprite = None
        self.parent.facing = 0
        self.parent.ai = None
        self.parent.name = f"{self.parent.name} Corpse"
        self.parent.render_order = RenderOrder.CORPSE
        self.parent.flying = False
        
        self.engine.message_log.add_message(death_message, death_message_color)
    
    def repair(self, amount: int) -> int:
        new_hull_value = self.hp + amount
        if new_hull_value > self.max_hp:
            new_hull_value = self.max_hp
        amount_repaired = new_hull_value - self.hp
        self.hp = new_hull_value
        return amount_repaired
    
    def take_damage(self, amount: int) -> None:
        self.hp -= amount
