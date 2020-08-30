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
    
    def get_fov(self, view, x, y):
        viewed_hexes = []
        center_coords = hex_to_cube(hexagon=Hex(column=x, row=y))
        viewed_hexes.append(Hex(column=x, row=y))
        current = center_coords
    
        for k in range(0, view):
            current = cube_neighbor(cube=current, direction=4)
    
        for i in range(0, 6):
            for j in range(0, view):
                cube_line = cube_line_draw(cube1=center_coords, cube2=current)
                for cube in cube_line:
                    hx = cube_to_hex(cube)
                    if hx not in viewed_hexes[1:]:
                        viewed_hexes.append(hx)
                        break
            
                current = cube_neighbor(current, i)
    
        viewed = []
        for tile in viewed_hexes:
            if (0 <= tile.col < self.width) and (0 <= tile.row < self.height):
                viewed.append((tile.col, tile.row))
        print(set(viewed))
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


# def get_fov(entity, game_map, game_time, game_weather, fog_view=0):
#     """
#     Returns the list of tiles that can be viewed by the given entity
#     :param entity: given entity on the map
#     :param game_map: the current GameMap (for terrain)
#     :param game_time: current game Time (darkness effects view distance)
#     :param game_weather: current map Weather (bad weather effects view distance)
#     :param fog_view: int value of how many fog banks it takes to block line of sight
#     :return: list of tiles in view
#     """
#     view = entity.view
#     view += game_time.get_time_of_day_info['view']
#     view += game_weather.get_weather_info['view']
#     if entity.owner.wings:
#         view += 1
#     # account for phases of the moon
#     if not (6 <= game_time.hrs < 18):
#         if (13 < game_time.day < 18) \
#                 or (game_time.day == 13 and game_time.hrs >= 18) \
#                 or (game_time.day == 18 and game_time.hrs < 6):
#             view -= 1
#         elif (game_time.day > 28 or game_time.day < 3) \
#                 or (game_time.day == 28 and game_time.hrs >= 18) \
#                 or (game_time.day == 3 and game_time.hrs < 6):
#             view += 1
#     if view < 1:
#         view = 1
#
#     viewed_hexes = []
#     center_coords = hex_to_cube(hexagon=Hex(column=entity.owner.x, row=entity.owner.y))
#     viewed_hexes.append(Hex(column=entity.owner.x, row=entity.owner.y))
#     current = center_coords
#
#     for k in range(0, view):
#         current = cube_neighbor(cube=current, direction=4)
#
#     for i in range(0, 6):
#         for j in range(0, view):
#             cube_line = cube_line_draw(cube1=center_coords, cube2=current)
#             fog = 0
#             for cube in cube_line:
#                 hx = cube_to_hex(cube)
#                 if game_map.in_bounds(hx.col, hx.row) and game_map.terrain[hx.col][hx.row].fog:
#                     fog += 1
#                 if hx not in viewed_hexes[1:]:
#                     viewed_hexes.append(hx)
#                 if game_map.in_bounds(hx.col, hx.row) \
#                         and ((Elevation.SHALLOWS < game_map.terrain[hx.col][hx.row].elevation
#                               and not entity.owner.wings)
#                              or fog > fog_view):
#                     break
#
#             current = cube_neighbor(current, i)
#
#     viewed = []
#     for tile in viewed_hexes:
#         if (0 <= tile.col < game_map.width) and (0 <= tile.row < game_map.height):
#             viewed.append((tile.col, tile.row))
#     view_set = set(viewed)
#
#     return view_set
