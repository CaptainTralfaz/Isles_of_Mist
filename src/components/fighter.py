from components.base import BaseComponent
from entity import Actor
from game_map import Elevation
from input_handlers import GameOverEventHandler
from render_functions import RenderOrder


class Fighter(BaseComponent):
    parent: Actor
    
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power
    
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
            self.parent.icon = "sunken_ship"
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.parent.name} is dead!"
            if self.game_map.terrain[self.parent.x][self.parent.y].elevation < Elevation.SHALLOWS:
                self.parent.icon = "carcass"
            else:
                self.parent.icon = None
        
        self.parent.facing = 0
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE
        self.parent.view.distance = 0
        self.parent.flying = False
        
        print(death_message)
