from __future__ import annotations

from typing import Iterable, List, Tuple, TYPE_CHECKING

from pygame import display, image

from entity_factory import images
from render_functions import get_rotated_image
from tile import Elevation, Terrain, tile_size
from utilities import Hex, cube_directions, cube_add, cube_to_hex, hex_to_cube

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine

ocean = image.load("assets/ocean.png")
water = image.load("assets/water.png")
shallows = image.load("assets/shallows.png")
beach = image.load("assets/beach.png")
grass = image.load("assets/grass.png")
jungle = image.load("assets/jungle.png")
mountain = image.load("assets/mountain.png")
volcano = image.load("assets/volcano.png")


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = (), terrain=None):
        """
        The GameMap object, which holds the game map, map width, map height, tile information
        :param width: width of the game map
        :param height: height of the game map
        :param terrain: list of lists of Terrain tiles
        """
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = set(entities)
        
        if terrain:
            self.terrain = terrain
        else:
            self.terrain = [[Terrain(elevation=Elevation.OCEAN, explored=False) for y in range(height)] for x in
                            range(width)]
    
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def can_sail_to(self, x: int, y: int) -> bool:
        return self.terrain[x][y].elevation < Elevation.BEACH
    
    def render(self, main_display: display) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if self.terrain[x][y].explored:
                    if self.terrain[x][y].elevation == Elevation.OCEAN:
                        tile = ocean
                    elif self.terrain[x][y].elevation == Elevation.WATER:
                        tile = water
                    elif self.terrain[x][y].elevation == Elevation.SHALLOWS:
                        tile = shallows
                    elif self.terrain[x][y].elevation == Elevation.BEACH:
                        tile = beach
                    elif self.terrain[x][y].elevation == Elevation.GRASS:
                        tile = grass
                    elif self.terrain[x][y].elevation == Elevation.JUNGLE:
                        tile = jungle
                    elif self.terrain[x][y].elevation == Elevation.MOUNTAIN:
                        tile = mountain
                    else:
                        tile = volcano
                    # TODO magic numbers
                    #  (10 is the difference between the standard Tile size (32) and the Terrain tile size (42)
                    #  16 is half the vertical standard Tile size - offset is due to hexes
                    main_display.blit(tile, (x * tile_size - 10, y * tile_size + x % 2 * tile_size // 2 - 10 - 16))
        
        for entity in self.entities:
            main_display.blit(get_rotated_image(images[entity.icon], entity.facing),
                              (entity.x - 5, entity.y - 16 + ((entity.x // tile_size) % 2) * tile_size // 2))


def get_hex_water_neighbors(game_map: GameMap, x: int, y: int) -> List[Tuple[int, int]]:
    """
    Returns neighboring water tiles of a given (x, y) map coordinate
    :param game_map: GameMap
    :param x: int x of the game map coordinate
    :param y: int y of the game map coordinate
    :return: list of tile coordinate (x, y) tuples
    """
    neighbors = []
    for direction in cube_directions:
        start_cube = hex_to_cube(hexagon=Hex(column=x, row=y))
        neighbor_hex = cube_to_hex(cube=cube_add(cube1=start_cube, cube2=direction))
        if game_map.in_bounds(neighbor_hex.col, neighbor_hex.row) \
                and game_map.terrain[neighbor_hex.col][neighbor_hex.row].elevation < Elevation.BEACH:
            neighbors.append((neighbor_hex.col, neighbor_hex.row))
    return neighbors
