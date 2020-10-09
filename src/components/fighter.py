from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from components.base import BaseComponent
from constants.constants import move_elevations
from constants.enums import GameStates, RenderOrder
from event_handlers.player_dead import GameOverEventHandler

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor
    
    def __init__(self, hp: int, defense: int, power: int, name: str = "body",
                 can_hit: dict = None, max_hp: int = None):
        self.max_hp = hp if max_hp is None else max_hp
        self._hp = hp
        self.defense = defense
        self.power = power
        self.name = name
        if can_hit is None:
            self.can_hit = {"hull": 50, "sail": 20, "crew": 10, "weapon": 10, "cargo": 10}
        else:
            self.can_hit = can_hit
    
    def to_json(self) -> Dict:
        return {
            'max_hp': self.max_hp,
            'hp': self._hp,
            'defense': self.defense,
            'power': self.power,
            'name': self.name,
            'can_hit': self.can_hit
        }
    
    @staticmethod
    def from_json(json_data: Dict) -> Fighter:
        max_hp = json_data.get('max_hp')
        hp = json_data.get('_hp')
        defense = json_data.get('defense')
        power = json_data.get('power')
        name = json_data.get('name')
        can_hit = json_data.get('can_hit')
        return Fighter(hp=hp, defense=defense, power=power, name=name, can_hit=can_hit, max_hp=max_hp)

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
            self.engine.game_state = GameStates.PLAYER_DEAD
            death_message_color = 'red'
        else:
            death_message = f"{self.parent.name} is dead!"
            if self.game_map.terrain[self.parent.x][self.parent.y].elevation in move_elevations["water"]:
                self.parent.icon = "carcass"
            else:
                self.parent.icon = None
            death_message_color = 'orange'
            self.parent.view = None
        
        if self.parent.sprite:
            self.parent.sprite = None
        self.parent.facing = 0
        self.parent.ai = None
        self.parent.name = f"{self.parent.name} Corpse"
        self.parent.render_order = RenderOrder.CORPSE
        self.parent.flying = False
        
        self.engine.message_log.add_message(death_message, text_color=death_message_color)
    
    def repair(self, amount: int) -> int:
        new_hull_value = self.hp + amount
        if new_hull_value > self.max_hp:
            new_hull_value = self.max_hp
        amount_repaired = new_hull_value - self.hp
        self.hp = new_hull_value
        return amount_repaired
    
    def take_damage(self, amount: int) -> None:
        self.hp -= amount
