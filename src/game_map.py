from __future__ import annotations

from typing import Iterable, List, Tuple, TYPE_CHECKING

from pygame import display, image

from entity_factory import images
from render_functions import get_rotated_image
from tile import Elevation, Terrain, tile_size
from utilities import Hex, cube_directions, cube_add, cube_to_hex, hex_to_cube, cube_neighbor, cube_line_draw

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
fog_of_war = image.load("assets/fog_of_war.png")


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
    
    @property
    def game_map(self) -> GameMap:
        return self
    
    # TODO add fog LOS Blocking
    def get_ocean_fov(self, distance, x, y):
        viewed_hexes = []
        center_coords = hex_to_cube(hexagon=Hex(column=x, row=y))
        viewed_hexes.append(Hex(column=x, row=y))
        current = center_coords
    
        # set up starting cube
        for k in range(0, distance):
            current = cube_neighbor(cube=current, direction=4)
    
        for i in range(0, 6):
            for j in range(0, distance):
                cube_line = cube_line_draw(cube1=center_coords, cube2=current)
                
                previous_elevation = Elevation.OCEAN
                for cube in cube_line:
                    hx = cube_to_hex(cube)
                    if self.in_bounds(hx.col, hx.row) \
                            and self.terrain[hx.col][hx.row].elevation < previous_elevation:
                        break
                    if self.in_bounds(hx.col, hx.row):
                        previous_elevation = self.terrain[hx.col][hx.row].elevation
                    if self.in_bounds(hx.col, hx.row) \
                            and self.terrain[hx.col][hx.row].elevation <= Elevation.SHALLOWS:
                        previous_elevation = Elevation.OCEAN
                        
                    if hx not in viewed_hexes[1:]:
                        viewed_hexes.append(hx)
                        
                current = cube_neighbor(current, i)
                
        viewed = []
        for tile in viewed_hexes:
            if (0 <= tile.col < self.width) and (0 <= tile.row < self.height):
                viewed.append((tile.col, tile.row))
        return set(viewed)

    # TODO add FOG LOS BLOCKING
    def get_flying_fov(self, distance, x, y):
        viewed_hexes = []
        center_coords = hex_to_cube(hexagon=Hex(column=x, row=y))
        viewed_hexes.append(Hex(column=x, row=y))
        current = center_coords
    
        # set up starting cube
        for k in range(0, distance):
            current = cube_neighbor(cube=current, direction=4)
    
        for i in range(0, 6):
            for j in range(0, distance):
                cube_line = cube_line_draw(cube1=center_coords, cube2=current)
            
                for cube in cube_line:
                    hx = cube_to_hex(cube)
                    if hx not in viewed_hexes[1:]:
                        viewed_hexes.append(hx)
            
                current = cube_neighbor(current, i)
    
        viewed = []
        for tile in viewed_hexes:
            if (0 <= tile.col < self.width) and (0 <= tile.row < self.height):
                viewed.append((tile.col, tile.row))
        return set(viewed)

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
                    main_display.blit(tile, map_to_surface_coords_terrain(x, y))
        
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.engine.player.view.fov:
                    main_display.blit(fog_of_war, map_to_surface_coords_terrain(x, y))

        for entity in self.entities:
            if (entity.x, entity.y) in self.engine.player.view.fov:
                main_display.blit(get_rotated_image(images[entity.icon], entity.facing),
                                  map_to_surface_coords_entities(entity.x, entity.y))

    def get_path(self, x1: int, y1: int, x2: int, y2: int, flying: bool = False) -> List[Tuple[int, int]]:
        pass


# TODO magic numbers
#  (10 is the difference between the standard Tile size (32) and the Terrain tile size (42)
#  16 is half the vertical standard Tile size - offset is due to hexes
def map_to_surface_coords_terrain(x: int, y: int) -> Tuple[int, int]:
    terrain_overlap = 10
    half_hex_terrain_height = 16
    half_hex_terrain_width = 16
    return (x * tile_size - terrain_overlap,
            y * tile_size + x % 2 * half_hex_terrain_width - half_hex_terrain_height - terrain_overlap)


def map_to_surface_coords_entities(x: int, y: int) -> Tuple[int, int]:
    half_terrain_overlap = 5
    half_hex_terrain_height = 16
    return (x * tile_size - half_terrain_overlap,
            y * tile_size + x % 2 * half_hex_terrain_height - half_hex_terrain_height)


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
