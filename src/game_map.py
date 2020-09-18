from __future__ import annotations

from queue import Queue
from typing import Iterable, List, Tuple, TYPE_CHECKING

from pygame import display, Surface

from constants import colors
from constants import images, tile_size
from render_functions import get_rotated_image, render_border
from tile import Elevation, Terrain
from ui import view_port, DisplayInfo, margin, block_size
from utilities import Hex, cube_directions, cube_add, cube_to_hex, hex_to_cube, cube_neighbor, cube_line_draw

if TYPE_CHECKING:
    from entity import Actor
    from engine import Engine


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
    
    def render_mini(self, main_display: display, ui_layout: DisplayInfo) -> None:
        mini_surf = Surface((ui_layout.mini_width, ui_layout.mini_height))
        block = Surface((block_size, block_size))
        for x in range(self.width):
            for y in range(self.height):
                if self.terrain[x][y].explored:
                    block.fill(colors[self.terrain[x][y].elevation.name.lower()])
                    mini_surf.blit(block, (margin + x * block_size,
                                           margin + y * block_size + (x % 2) * block_size // 2 - 2))
        
        for entity in self.entities:
            if (entity.x, entity.y) in self.engine.player.view.fov \
                    and entity.icon is not None:
                if entity == self.engine.player:
                    block.fill(colors["white"])
                elif entity.is_alive:
                    block.fill(colors["player_die"])
                else:
                    block.fill(colors["enemy_die"])
                mini_surf.blit(block, (margin + entity.x * block_size,
                                       margin + entity.y * block_size + (entity.x % 2) * block_size // 2 - 2))
        
        render_border(mini_surf, color=colors['white'])
        main_display.blit(mini_surf, (0, 0))
    
    def render(self, main_display: display, ui_layout: DisplayInfo) -> None:
        half_tile = tile_size // 2
        
        left = self.engine.player.x - view_port
        right = left + 2 * view_port + 1
        
        top = self.engine.player.y - view_port - 1
        bottom = top + 2 * view_port + 3
        
        map_surf = Surface(((2 * view_port + 1) * tile_size, (2 * view_port + 1) * tile_size + 2 * margin))
        offset = self.engine.player.x % 2 * half_tile
        
        for x in range(left, right):
            for y in range(top, bottom):
                if self.in_bounds(x, y) and self.terrain[x][y].explored:
                    
                    if self.terrain[x][y].elevation == Elevation.OCEAN:
                        tile = 'ocean'
                    elif self.terrain[x][y].elevation == Elevation.WATER:
                        tile = 'water'
                    elif self.terrain[x][y].elevation == Elevation.SHALLOWS:
                        tile = 'shallows'
                    elif self.terrain[x][y].elevation == Elevation.BEACH:
                        tile = 'beach'
                    elif self.terrain[x][y].elevation == Elevation.GRASS:
                        tile = 'grass'
                    elif self.terrain[x][y].elevation == Elevation.JUNGLE:
                        tile = 'jungle'
                    elif self.terrain[x][y].elevation == Elevation.MOUNTAIN:
                        tile = 'mountain'
                    else:
                        tile = 'volcano'
                    
                    map_surf.blit(images[tile], ((x - left) * tile_size - margin,
                                                 (y - top - 1) * tile_size + x % 2 * half_tile - margin - offset))
        
        for x in range(left, right):
            for y in range(top, bottom):
                if (x, y) not in self.engine.player.view.fov:
                    map_surf.blit(images["fog_of_war"], ((x - left) * tile_size - margin,
                                                         (
                                                                 y - top - 1) * tile_size + x % 2 * half_tile - margin - offset))
        
        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda i: i.render_order.value
        )
        
        for entity in entities_sorted_for_rendering:
            if (entity.x, entity.y) in self.engine.player.view.fov \
                    and entity.icon is not None:
                map_surf.blit(get_rotated_image(images[entity.icon], entity.facing),
                              ((entity.x - left) * tile_size,
                               (entity.y - top - 1) * tile_size + entity.x % 2 * half_tile + margin - offset))
        
        render_border(map_surf, (255, 255, 255))
        main_display.blit(map_surf, (ui_layout.mini_width, 0))
    
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
    
    def get_targets_at_location(self, grid_x: int, grid_y: int, living_targets: bool = True) -> List[Actor]:
        targets = []
        for entity in self.entities:
            if entity.x == grid_x and entity.y == grid_y:
                if living_targets:
                    if entity.is_alive:
                        targets.append(entity)
                else:
                    targets.append(entity)
        return targets
    
    @staticmethod
    def surface_to_map_coords(x: int, y: int, player_x: int) -> Tuple[int, int]:
        half_tile_size = tile_size // 2
        x_grid = x // tile_size
        y_grid = (y + 2 * margin - half_tile_size
                  + (player_x % 2) * half_tile_size
                  - ((player_x - x_grid) % 2) * half_tile_size
                  ) // tile_size
        
        return x_grid, y_grid
