from __future__ import annotations

import copy
from typing import Optional, Type, TypeVar, TYPE_CHECKING

from utilities import Hex, hex_to_cube, cube_to_hex, cube_neighbor, direction_angle

if TYPE_CHECKING:
    from game_map import GameMap
    from components.ai import BaseAI
    from components.fighter import Fighter
    from components.view import View
    
T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    parent: GameMap
    
    def __init__(self, x: int,
                 y: int,
                 facing: int,
                 icon: str,
                 parent: Optional[GameMap] = None,
                 name: str = "<Unnamed>"):
        self.x = x
        self.y = y
        self.facing = facing  # TODO move to Actor
        self.icon = icon
        self.name = name
        if parent:
            self.parent = parent
            parent.entities.add(self)

    @property
    def game_map(self) -> GameMap:
        return self.parent.game_map
    
    def spawn(self: T, game_map: GameMap, x: int, y: int, facing: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.facing = facing
        clone.parent = game_map
        game_map.entities.add(clone)
        return clone
    
    def move(self) -> None:
        old_cube = hex_to_cube(Hex(self.x, self.y))
        new_hex = cube_to_hex(cube_neighbor(old_cube, self.facing))
        self.x = new_hex.col
        self.y = new_hex.row
    
    def rotate(self, direction: int):
        self.facing += direction
        if self.facing >= len(direction_angle):
            self.facing = 0
        elif self.facing < 0:
            self.facing = len(direction_angle) - 1

    def get_next_hex(self):
        old_cube = hex_to_cube(Hex(self.x, self.y))
        new_hex = cube_to_hex(cube_neighbor(old_cube, self.facing))
        return new_hex.col, new_hex.row
    
    def place(self, x: int, y: int, game_map: Optional[GameMap] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "parent"):  # Possibly uninitialized
                self.game_map.entities.remove(self)
            self.parent = game_map
            game_map.entities.add(self)


class Actor(Entity):
    def __init__(self,
                 *,
                 ai_cls: Type[BaseAI],
                 fighter: Fighter,
                 view: View,
                 x: int = 0,
                 y: int = 0,
                 facing: int = 0,
                 icon: str = "",
                 name: str = "<Unnamed>"):
        super().__init__(
            x=x,
            y=y,
            facing=facing,
            icon=icon,
            name=name,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)
        self.fighter = fighter
        self.fighter.parent = self
        self.view = view
        self.view.parent = self
        
    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)


