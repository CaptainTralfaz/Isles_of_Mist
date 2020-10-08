from __future__ import annotations

import copy
from typing import Optional, Dict, Type, TypeVar, TYPE_CHECKING

from constants.enums import RenderOrder
from utilities import Hex, hex_to_cube, cube_to_hex, cube_neighbor, direction_angle

if TYPE_CHECKING:
    from game_map import GameMap
    from components.ai import BaseAI
    from components.broadsides import Broadsides
    from components.cargo import Cargo
    from components.crew import Crew
    from components.fighter import Fighter
    from components.sails import Sails
    from components.view import View
    from sprite import Sprite
    
# noinspection
T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    parent: GameMap
    
    def __init__(self, x: int,
                 y: int,
                 icon: str,
                 elevations: str,
                 sprite: Optional[Sprite] = None,
                 parent: Optional[GameMap] = None,
                 cargo: Optional[Cargo] = None,
                 name: str = "<Unnamed>",
                 render_order: RenderOrder = RenderOrder.FLOATER):
        self.x = x
        self.y = y
        self.icon = icon
        self.sprite = sprite
        self.name = name
        self.render_order = render_order
        self.elevations = elevations
        if parent:
            self.parent = parent
            parent.entities.add(self)
        self.fighter = None
        if cargo:
            self.cargo = cargo
            self.cargo.parent = self
    
    @property
    def is_alive(self) -> bool:
        """Returns True as long as this entity can perform actions."""
        return False
    
    @property
    def game_map(self) -> GameMap:
        return self.parent.game_map

    def to_json(self) -> Dict:
        return {
            'x': self.x,
            'y': self.y,
            'icon': self.icon if self.icon is not None else None,
            'sprite': self.sprite.sprite_name if self.sprite is not None else None,
            'name': self.name,
            'render_order': self.render_order.value,
            'elevations': self.elevations,
            'cargo': self.cargo.to_json() if self.cargo is not None else None
        }
    
    def spawn(self: T, game_map: GameMap, x: int, y: int, facing: int = None) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.facing = facing
        clone.parent = game_map
        game_map.entities.add(clone)
        return clone
    
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
                 ai_cls: Type[BaseAI] = None,
                 fighter: Fighter,
                 sails: Sails = None,
                 crew: Crew = None,
                 cargo: Cargo = None,
                 broadsides: Broadsides = None,
                 view: View,
                 x: int = 0,
                 y: int = 0,
                 elevations: str,
                 facing: int = 0,
                 icon: str = "",
                 sprite: Optional[Sprite] = None,
                 name: str = "<Unnamed>",
                 flying: bool = False,
                 render_order: RenderOrder = RenderOrder.SWIMMER):
        super().__init__(
            x=x,
            y=y,
            elevations=elevations,
            icon=icon,
            cargo=cargo,
            sprite=sprite,
            name=name,
            render_order=render_order)
        
        self.ai: Optional[BaseAI] = ai_cls(self)
        self.fighter = fighter
        if fighter:
            self.fighter.parent = self
        self.sails = sails
        if sails:
            self.sails.parent = self
        self.crew = crew
        if crew:
            self.crew.parent = self
        self.broadsides = broadsides
        if broadsides:
            self.broadsides.parent = self
        self.view = view
        self.view.parent = self
        self.flying = flying
        self.facing = facing
        if self.flying:
            self.render_order = RenderOrder.FLYER
        elif self.name == "Player":
            self.render_order = RenderOrder.PLAYER
        else:
            self.render_order = RenderOrder.SWIMMER
    
    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
    
    def to_json(self) -> Dict:
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'icon': self.icon if self.icon is not None else None,
            'sprite': self.sprite.sprite_name if self.sprite is not None else None,
            'render_order': self.render_order.value,
            'elevations': self.elevations,
            'cargo': self.cargo.to_json() if self.cargo is not None else None,
            'ai': self.ai.to_json() if self.ai is not None else None,
            'fighter': self.fighter.to_json() if self.fighter is not None else None,
            'sails': self.sails.to_json() if self.sails is not None else None,
            'crew': self.crew.to_json() if self.crew is not None else None,
            'broadsides': self.broadsides.to_json() if self.broadsides is not None else None,
            'view': self.view.to_json() if self.view is not None else None,
            'facing': self.facing,
            'flying': self.cargo.to_json(),
        }

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
