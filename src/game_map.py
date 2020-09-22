from __future__ import annotations

from queue import Queue
from typing import Iterable, List, Tuple, TYPE_CHECKING

from pygame import display, Surface

from constants import block_size, colors, images, margin, sprites, tile_size, view_port
from render_functions import get_rotated_image, render_border
from tile import Elevation, Terrain
from ui import DisplayInfo
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
    
    def can_sail_to(self, x: int, y: int) -> bool:
        return self.terrain[x][y].elevation <= Elevation.SHALLOWS
    
    def can_fly_to(self, x: int, y: int) -> bool:
        return self.terrain[x][y].elevation <= Elevation.JUNGLE
    
    def render_mini(self, main_display: display, ui_layout: DisplayInfo) -> None:
        mini_surf = Surface((ui_layout.mini_width, ui_layout.mini_height))
        block = Surface((block_size, block_size))
        mini_block = Surface((block_size // 2, block_size // 2))
        for x in range(self.width):
            for y in range(self.height):
                if self.terrain[x][y].explored:
                    block.fill(colors[self.terrain[x][y].elevation.name.lower()])
                    mini_surf.blit(block, (margin + x * block_size,
                                           margin + y * block_size + (x % 2) * block_size // 2 - 2))
                    if self.terrain[x][y].decoration:
                        mini_block.fill(colors[self.terrain[x][y].decoration])
                        mini_surf.blit(mini_block,
                                       (margin + 1 + x * block_size,
                                        margin + 1 + y * block_size + (x % 2) * block_size // 2 - 2))
        
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
        
        render_border(mini_surf, self.engine.time.get_sky_color)
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
                    map_surf.blit(images[self.terrain[x][y].elevation.name.lower()],
                                  ((x - left) * tile_size - margin,
                                   (y - top - 1) * tile_size + (x % 2) * half_tile - margin - offset))
                    if self.terrain[x][y].decoration:
                        map_surf.blit(images[self.terrain[x][y].decoration],
                                      ((x - left) * tile_size,
                                       (y - top - 1) * tile_size + (x % 2) * half_tile + margin - offset))
                    # coord_text = game_font.render(f"{x}:{y}", False, (0, 0, 0))
                    # map_surf.blit(coord_text,
                    #               ((x - left) * tile_size,
                    #                (y - top - 1) * tile_size + (x % 2) * half_tile + half_tile - offset))
        
        for x in range(left, right):
            for y in range(top, bottom):
                if (x, y) not in self.engine.player.view.fov:
                    map_surf.blit(images["fog_of_war"],
                                  ((x - left) * tile_size - margin,
                                   (y - top - 1) * tile_size + (x % 2) * half_tile - margin - offset))
        
        if self.engine.key_mod:
            if self.engine.key_mod == "shift":
                target_tiles = self.engine.game_map.get_neighbors(self.engine.player.x,
                                                                  self.engine.player.y,
                                                                  Elevation.VOLCANO)
                target_tiles.append((self.engine.player.x, self.engine.player.y))
                for (x, y) in target_tiles:
                    map_surf.blit(images["highlight"],
                                  ((x - left) * tile_size - margin,
                                   (y - top - 1) * tile_size + (x % 2) * half_tile - margin - offset))
        
        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda i: i.render_order.value
        )
        
        for entity in entities_sorted_for_rendering:
            if entity.sprite and (entity.x, entity.y) in self.engine.player.view.fov:
                entity.sprite.update(self.engine.clock.get_fps())
                map_surf.blit(get_rotated_image(sprites[entity.sprite.sprite_name][entity.sprite.pointer],
                                                entity.facing),
                              ((entity.x - left) * tile_size,
                               (entity.y - top - 1) * tile_size + (entity.x % 2) * half_tile + margin - offset))
            elif (entity.x, entity.y) in self.engine.player.view.fov and entity.icon is not None:
                map_surf.blit(get_rotated_image(images[entity.icon], entity.facing),
                              ((entity.x - left) * tile_size,
                               (entity.y - top - 1) * tile_size + (entity.x % 2) * half_tile + margin - offset))
        
        for x, y in self.engine.player.view.fov:
            if self.in_bounds(x, y) and self.terrain[x][y].mist:
                map_surf.blit(images["mist"],
                              ((x - left) * tile_size - margin,
                               (y - top - 1) * tile_size + (x % 2) * half_tile - margin - offset))
        
        render_border(map_surf, self.engine.time.get_sky_color)

        tint_surf = Surface(((2 * view_port + 1) * tile_size, (2 * view_port + 1) * tile_size + 2 * margin))
        tint_surf.set_alpha(abs(self.engine.time.hrs * 60 + self.engine.time.mins - 720) // 8)
        tint = self.engine.time.get_sky_color
        tint_surf.fill(tint)
        
        map_surf.blit(tint_surf, (0, 0))
        main_display.blit(map_surf, (ui_layout.mini_width, 0))
        
    def gen_distance_map(self,
                         target_x: int,
                         target_y: int,
                         flying: bool = False) -> dict:
        # TODO cut short when path is found?
        path_map = self.gen_path_map(target_x, target_y, flying)
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
    
    def gen_path_map(self, target_x: int, target_y: int, flying: bool) -> dict:
        frontier = Queue()
        frontier.put((target_x, target_y))
        came_from = dict()
        came_from[(target_x, target_y)] = None
        
        while not frontier.empty():
            current = frontier.get()
            x, y = current
            elevation = Elevation.MOUNTAIN if flying else Elevation.BEACH
            for neighbor in self.get_neighbors(x=x, y=y, elevation=elevation):
                if neighbor not in came_from:
                    frontier.put(neighbor)
                    came_from[(neighbor[0], neighbor[1])] = current
        return came_from
    
    def get_neighbors(self, x, y, elevation: Elevation = Elevation.BEACH, below: bool = True) -> List[Tuple[int, int]]:
        neighbors = []
        for direction in cube_directions:
            start_cube = hex_to_cube(hexagon=Hex(column=x, row=y))
            neighbor_hex = cube_to_hex(cube=cube_add(cube1=start_cube, cube2=direction))
            if self.in_bounds(neighbor_hex.col, neighbor_hex.row):
                if below:
                    if self.terrain[neighbor_hex.col][neighbor_hex.row].elevation < elevation:
                        neighbors.append((neighbor_hex.col, neighbor_hex.row))
                else:  # above
                    if self.terrain[neighbor_hex.col][neighbor_hex.row].elevation >= elevation:
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
        
        y_grid = (y - margin - margin // 2
                  # even and odd
                  + half_tile_size * (player_x % 2)
                  # odd viewport
                  - (view_port % 2) * half_tile_size
                  + (view_port % 2) * half_tile_size * ((x_grid + player_x) % 2)
                  # even viewport
                  - ((view_port + 1) % 2) * half_tile_size * ((x_grid + player_x) % 2)
                  ) // tile_size
        return x_grid, y_grid
