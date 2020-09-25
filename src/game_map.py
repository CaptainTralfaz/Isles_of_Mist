from __future__ import annotations

from queue import Queue
from typing import Iterable, List, TYPE_CHECKING

from constants import view_port
from tile import Elevation, Terrain
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
            self.terrain = [[Terrain(elevation=Elevation.OCEAN, explored=False) for y in range(height)]
                            for x in range(width)]
        self.port = None
    
    @property
    def game_map(self) -> GameMap:
        return self
    
    def get_fov(self, distance, x, y, elevation, mist_view=1):
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
                mist_count = 0
                
                previous_elevation = elevation
                for cube in cube_line:
                    hx = cube_to_hex(cube)
                    if not self.in_bounds(hx.col, hx.row):
                        break
                    else:
                        current_elevation = self.terrain[hx.col][hx.row].elevation
                    
                    if self.in_bounds(hx.col, hx.row) \
                            and current_elevation <= elevation:
                        current_elevation = elevation
                    if self.in_bounds(hx.col, hx.row) \
                            and (current_elevation < previous_elevation
                                 or mist_count >= mist_view):
                        break
                    
                    if self.in_bounds(hx.col, hx.row) \
                            and self.terrain[hx.col][hx.row].mist:
                        mist_count += 1
                    previous_elevation = current_elevation
                    
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
    
    def can_move_to(self, x: int, y: int, elevations) -> bool:
        return self.terrain[x][y].elevation in elevations
    
    def gen_distance_map(self,
                         target_x: int,
                         target_y: int,
                         elevations: list) -> dict:
        # TODO cut short when path is found?
        path_map = self.gen_path_map(target_x, target_y, elevations)
        distance_map = dict()
        
        for w in range(max(0, target_x - view_port), min(self.width, (target_x + view_port))):
            for h in range(max(0, target_y - view_port), min(self.height, target_y + view_port)):
                path = []
                if path_map.get((w, h)):
                    current = (w, h)
                    while current != (target_x, target_y):
                        path.append(current)
                        if not current:
                            break
                        current = path_map[current]
                if path:
                    distance_map[(w, h)] = len(path)
        return distance_map
    
    def gen_path_map(self, target_x: int, target_y: int, elevations: list) -> dict:
        frontier = Queue()
        frontier.put((target_x, target_y))
        came_from = dict()
        came_from[(target_x, target_y)] = (target_x, target_y)
        
        while not frontier.empty():
            current = frontier.get()
            x, y = current
            for neighbor in self.get_neighbors_at_elevations(x=x, y=y, elevations=elevations):
                if neighbor not in came_from:
                    frontier.put(neighbor)
                    came_from[(neighbor[0], neighbor[1])] = current
        return came_from
    
    def get_neighbors_at_elevations(self, x, y, elevations):
        neighbors = []
        for direction in cube_directions:
            start_cube = hex_to_cube(hexagon=Hex(column=x, row=y))
            neighbor_hex = cube_to_hex(cube=cube_add(cube1=start_cube, cube2=direction))
            if self.in_bounds(neighbor_hex.col, neighbor_hex.row) \
                    and self.terrain[neighbor_hex.col][neighbor_hex.row].elevation in elevations:
                neighbors.append((neighbor_hex.col, neighbor_hex.row))
        return neighbors
    
    # def get_neighbors(self, x, y, elevation: Elevation = Elevation.BEACH, below: bool = True
    # ) -> List[Tuple[int, int]]:
    #     neighbors = []
    #     for direction in cube_directions:
    #         start_cube = hex_to_cube(hexagon=Hex(column=x, row=y))
    #         neighbor_hex = cube_to_hex(cube=cube_add(cube1=start_cube, cube2=direction))
    #         if self.in_bounds(neighbor_hex.col, neighbor_hex.row):
    #             if below:
    #                 if self.terrain[neighbor_hex.col][neighbor_hex.row].elevation < elevation:
    #                     neighbors.append((neighbor_hex.col, neighbor_hex.row))
    #             else:  # above
    #                 if self.terrain[neighbor_hex.col][neighbor_hex.row].elevation >= elevation:
    #                     neighbors.append((neighbor_hex.col, neighbor_hex.row))
    #     return neighbors
    
    def get_targets_at_location(self, grid_x: int, grid_y: int, living_targets: bool = True) -> List[Actor]:
        targets = []
        for entity in self.entities:
            if entity.x == grid_x and entity.y == grid_y:
                if living_targets:
                    if entity.is_alive:
                        targets.append(entity)
                else:
                    targets.append(entity)
        if self.engine.player in targets:
            targets.remove(self.engine.player)
        return targets
