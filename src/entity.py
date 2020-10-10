from __future__ import annotations

import copy
from typing import Optional, Dict, TypeVar, TYPE_CHECKING

from components.ai import ai_class
from components.broadsides import Broadsides
from components.cargo import Cargo
from components.crew import Crew
from components.fighter import Fighter
from components.sails import Sails
from components.view import View
from constants.enums import RenderOrder
from sprite import Sprite
from utilities import Hex, hex_to_cube, cube_to_hex, cube_neighbor, direction_angle

if TYPE_CHECKING:
    from game_map import GameMap

# noinspection
T = TypeVar("T", bound="Entity")


class Entity:
    parent: GameMap
    
    def __init__(self,
                 x: int,
                 y: int,
                 elevations: str,
                 name: str = "<Unnamed>",
                 icon: str = None,
                 sprite: Optional[Sprite] = None,
                 parent: Optional[GameMap] = None,
                 cargo: Optional[Cargo] = None,
                 ai_cls_name: str = None,
                 fighter: Fighter = None,
                 sails: Sails = None,
                 crew: Crew = None,
                 broadsides: Broadsides = None,
                 view: View = None,
                 facing: int = None,
                 flying: bool = False):
        
        self.x = x
        self.y = y
        self.elevations = elevations
        self.name = name
        self.icon = icon
        self.sprite = sprite
        self.cargo = cargo
        if self.cargo:
            self.cargo.parent = self
        self.ai = ai_class[ai_cls_name](self) if ai_cls_name is not None else None
        if parent:
            self.parent = parent
            parent.entities.add(self)
        self.fighter = fighter
        if self.fighter:
            self.fighter.parent = self
        self.sails = sails
        if self.sails:
            self.sails.parent = self
        self.crew = crew
        if self.crew:
            self.crew.parent = self
        self.broadsides = broadsides
        if self.broadsides:
            self.broadsides.parent = self
        self.view = view
        if self.view:
            self.view.parent = self
        self.facing = facing
        self.flying = flying
        if self.flying:
            self.render_order = RenderOrder.FLYER
        elif self.name == "Player":
            self.render_order = RenderOrder.PLAYER
        elif self.ai:
            self.render_order = RenderOrder.SWIMMER
        else:
            self.render_order = RenderOrder.FLOATER
    
    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
    
    @property
    def game_map(self) -> GameMap:
        return self.parent.game_map
    
    def to_json(self) -> Dict:
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'facing': self.facing,
            'flying': self.flying,
            'elevations': self.elevations,
            'view': self.view.to_json() if self.view is not None else None,
            'ai': self.ai.__class__.__name__ if self.ai is not None else None,
            'icon': self.icon if self.icon is not None else None,
            'sprite': self.sprite.to_json() if self.sprite is not None else None,
            'fighter': self.fighter.to_json() if self.fighter is not None else None,
            'sails': self.sails.to_json() if self.sails is not None else None,
            'crew': self.crew.to_json() if self.crew is not None else None,
            'broadsides': self.broadsides.to_json() if self.broadsides is not None else None,
            'cargo': self.cargo.to_json() if self.cargo is not None else None
        }
    
    @staticmethod
    def from_json(json_data) -> Entity:
        name = json_data.get('name')
        x = json_data.get('x')
        y = json_data.get('y')
        facing = json_data.get('facing')
        flying = json_data.get('flying')
        elevations = json_data.get('elevations')
        ai = json_data.get('ai')
        icon = json_data.get('icon')
        view = View.from_json(json_data.get('view')) \
            if json_data.get('view') is not None else None
        sprite = Sprite.from_json(json_data.get('sprite')) \
            if json_data.get('sprite') is not None else None
        fighter = Fighter.from_json(json_data.get('fighter')) \
            if json_data.get('fighter') is not None else None
        sails = Sails.from_json(json_data.get('sails')) \
            if json_data.get('sails') is not None else None
        crew = Crew.from_json(json_data.get('crew')) \
            if json_data.get('crew') is not None else None
        broadsides = Broadsides.from_json(json_data.get('broadsides')) \
            if json_data.get('broadsides') is not None else None
        cargo = Cargo.from_json(json_data.get('cargo')) \
            if json_data.get('cargo') is not None else None
        return Entity(name=name, x=x, y=y, facing=facing, flying=flying,
                      elevations=elevations, view=view, ai_cls_name=ai,
                      icon=icon, sprite=sprite, fighter=fighter, sails=sails,
                      crew=crew, broadsides=broadsides, cargo=cargo)
    
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
