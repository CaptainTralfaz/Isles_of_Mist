from pygame import Surface

from src.utilities import Hex, hex_to_cube, cube_to_hex, cube_neighbor, direction_angle
from src.tile import tile_size


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    
    def __init__(self, x: int, y: int, facing: int, icon: Surface):
        self.x = x
        self.y = y
        self.facing = facing
        self.icon = icon
    
    def move(self) -> None:
        old_cube = hex_to_cube(Hex(self.x // tile_size, self.y // tile_size))
        new_hex = cube_to_hex(cube_neighbor(old_cube, self.facing))
        self.x = new_hex.col * tile_size
        self.y = new_hex.row * tile_size
    
    def rotate(self, direction: int):
        self.facing += direction
        if self.facing >= len(direction_angle):
            self.facing = 0
        elif self.facing < 0:
            self.facing = len(direction_angle) - 1
    
    def get_next_hex(self):
        old_cube = hex_to_cube(Hex(self.x // tile_size, self.y // tile_size))
        new_hex = cube_to_hex(cube_neighbor(old_cube, self.facing))
        return new_hex.col, new_hex.row
