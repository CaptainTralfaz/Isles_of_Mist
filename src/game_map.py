from __future__ import annotations

from queue import Queue
from typing import Iterable, List, Tuple, TYPE_CHECKING

from pygame import display, image, font

from render_functions import get_rotated_image
from tile import Elevation, Terrain, tile_size
from utilities import images, Hex, cube_directions, cube_add, cube_to_hex, hex_to_cube, cube_neighbor, cube_line_draw

if TYPE_CHECKING:
    from entity import Actor
    from engine import Engine

font.init()

game_font = font.Font('freesansbold.ttf', 16)

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
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Actor] = (), terrain=None):
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
        return self.terrain[x][y].elevation <= Elevation.SHALLOWS
    
    def can_fly_to(self, x: int, y: int) -> bool:
        return self.terrain[x][y].elevation <= Elevation.JUNGLE
    
    def render(self, main_display: display) -> None:
        # sail_map = self.gen_sail_distance_map(self.engine.player.x, self.engine.player.y)
        # flying_map = self.gen_flying_distance_map(self.engine.player.x, self.engine.player.y)
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
                    # display distance maps
                    # xx, yy = map_to_surface_coords_terrain(x, y)
                    # if flying_map.get((x, y)):
                    #     main_display.blit(game_font.render("{}".format(flying_map[x, y]), True, (0, 0, 0)),
                    #                       (xx + 15, yy + 20))
        
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.engine.player.view.fov:
                    main_display.blit(fog_of_war, map_to_surface_coords_terrain(x, y))
        
        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda i: i.render_order.value
        )
        
        for entity in entities_sorted_for_rendering:
            if (entity.x, entity.y) in self.engine.player.view.fov \
                    and entity.icon is not None:
                main_display.blit(get_rotated_image(images[entity.icon], entity.facing),
                                  map_to_surface_coords_entities(entity.x, entity.y))
    
    def gen_distance_map(self, x: int, y: int, flying: bool = False) -> dict:
        if not flying:
            return self.gen_sail_distance_map(x, y)
        else:
            return self.gen_flying_distance_map(x, y)
    
    def gen_sail_distance_map(self, x: int, y: int) -> dict:
        sail_map = self.gen_sail_path_map(x, y)
        distance_sail_map = dict()
        
        for w in range(self.width):
            for h in range(self.height):
                path = []
                if sail_map.get((w, h)):
                    current = (w, h)
                    while current != (x, y):
                        path.append(current)
                        if not current:
                            break
                        current = sail_map[current]
                if path:
                    distance_sail_map[(w, h)] = len(path)
        return distance_sail_map
    
    def gen_flying_distance_map(self, x: int, y: int) -> dict:
        flying_map = self.gen_flying_path_map(x, y)
        distance_flying_map = dict()
        
        for w in range(self.width):
            for h in range(self.height):
                path = []
                if flying_map.get((w, h)):
                    current = (w, h)
                    while current != (x, y):
                        path.append(current)
                        if not current:
                            break
                        current = flying_map[current]
                if path:
                    distance_flying_map[(w, h)] = len(path)
        return distance_flying_map
    
    def gen_sail_path_map(self, x: int, y: int) -> dict:
        frontier = Queue()
        frontier.put((x, y))
        came_from = dict()
        came_from[(x, y)] = None
        
        while not frontier.empty():
            current = frontier.get()
            x, y = current
            for neighbor in self.get_water_neighbors(x=x, y=y):
                if neighbor not in came_from:
                    frontier.put(neighbor)
                    came_from[(neighbor[0], neighbor[1])] = current
        return came_from
    
    def gen_flying_path_map(self, x: int, y: int) -> dict:
        frontier = Queue()
        frontier.put((x, y))
        came_from = dict()
        came_from[(x, y)] = None
        
        while not frontier.empty():
            current = frontier.get()
            x, y = current
            for neighbor in self.get_neighbors(x=x, y=y):
                if neighbor not in came_from:
                    frontier.put(neighbor)
                    came_from[(neighbor[0], neighbor[1])] = current
        return came_from
    
    def get_neighbors(self, x, y) -> List[Tuple[int, int]]:
        neighbors = []
        for direction in cube_directions:
            start_cube = hex_to_cube(hexagon=Hex(column=x, row=y))
            neighbor_hex = cube_to_hex(cube=cube_add(cube1=start_cube, cube2=direction))
            if self.in_bounds(neighbor_hex.col, neighbor_hex.row):
                neighbors.append((neighbor_hex.col, neighbor_hex.row))
        return neighbors
    
    def get_water_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for direction in cube_directions:
            start_cube = hex_to_cube(hexagon=Hex(column=x, row=y))
            neighbor_hex = cube_to_hex(cube=cube_add(cube1=start_cube, cube2=direction))
            if self.in_bounds(neighbor_hex.col, neighbor_hex.row) \
                    and self.terrain[neighbor_hex.col][neighbor_hex.row].elevation < Elevation.BEACH:
                neighbors.append((neighbor_hex.col, neighbor_hex.row))
        return neighbors
    
    def get_targets_at_location(self, x: int, y: int) -> List[Actor]:
        targets = []
        for entity in self.entities:
            if entity.x == x and entity.y == y and entity.is_alive:
                targets.append(entity)
        return targets


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
