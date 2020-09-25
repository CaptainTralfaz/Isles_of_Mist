from components.base import BaseComponent
from constants import colors
from entity import Actor
from game_map import Elevation
from input_handlers import GameOverEventHandler
from render_functions import RenderOrder


class Crew(BaseComponent):
    parent: Actor
    
    def __init__(self, count: int, max_count: int, defense: int, name: str = "crew"):
        self.max_count = max_count
        self._count = count
        self.defense = defense
        self.name = name
    
    @property
    def count(self) -> int:
        return self._count
    
    @count.setter
    def count(self, value: int) -> None:
        self._count = max(0, min(value, self.max_count))
        if self._count == 0 and self.parent.ai:
            self.die()
    
    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "All your crew are dead! Game Over!"
            self.parent.icon = "shipwreck"
            self.engine.event_handler = GameOverEventHandler(self.engine)
            death_message_color = colors['red']
        else:
            death_message = f"{self.parent.name} has no crew left!"
            if self.game_map.terrain[self.parent.x][self.parent.y].elevation < Elevation.BEACH:
                self.parent.icon = "carcass"
            else:
                self.parent.icon = None
            death_message_color = colors['orange']
        
        self.parent.facing = 0
        self.parent.ai = None
        self.parent.name = f"{self.parent.name} Corpse"
        self.parent.render_order = RenderOrder.CORPSE
        self.parent.view.distance = 0
        self.parent.flying = False
        
        self.engine.message_log.add_message(death_message, death_message_color)
    
    def heal(self, amount: int) -> int:
        if self.count == self.max_count:
            return 0
        new_crew_value = self.count + amount
        if new_crew_value > self.max_count:
            new_crew_value = self.max_count
        amount_recovered = new_crew_value - self.count
        self.count = new_crew_value
        return amount_recovered
    
    def take_damage(self, amount: int) -> None:
        self.count -= amount
