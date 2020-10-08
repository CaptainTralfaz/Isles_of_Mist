from __future__ import annotations

from queue import Queue
from random import randint
from typing import Iterable, List, Tuple, Optional, Set, Dict, TYPE_CHECKING

from constants.colors import colors
from constants.enums import Conditions, Elevation
from port import Port
from tile import Terrain
from utilities import Hex, cube_directions, cube_add, cube_to_hex, \
    hex_to_cube, cube_neighbor, cube_line_draw, get_distance

if TYPE_CHECKING:
    from entity import Entity, Actor
    from engine import Engine
    from weather import Weather


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, weather: Weather = None,
                 entities: Iterable[Entity] = (), terrain=None):
        """
        The GameMap object, which holds the game map, map width, map height, tile information
        :param engine: Parent of the game map
        :param width: width of the game map
        :param height: height of the game map
        :param entities: list of Entity objects with locations on the game map
        :param terrain: list of lists of Terrain tiles
        """
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = set(entities)
        self.weather = weather
        
        if terrain:
            self.terrain = terrain
        else:
            self.terrain = [[Terrain(elevation=Elevation.OCEAN, explored=False) for y in range(height)]
                            for x in range(width)]
        self.port = Port()
    
    @property
    def game_map(self) -> GameMap:
        return self
    
    def get_fov(self,
                distance: int,
                x: int,
                y: int,
                elevation: Elevation,
                mist_view: int = 1
                ) -> Set[Tuple[int, int]]:
        """
        Returns a set of (x, y) coordinates within view distance and less than the maximum elevation
        :param distance: int distance from center to check
        :param x: x int coordinate of game map
        :param y: y int coordinate of game map
        :param elevation: Elevation enum
        :param mist_view: max number of mist hexes that cannot be viewed beyond
        :return: set of Tuple (x, y) coordinates that can be seen
        """
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
        """
        Return True if x and y are inside of the bounds of this map.
        :param x: x int coordinate of game map
        :param y: y int coordinate of game map
        :return: bool
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def can_move_to(self, x: int, y: int, elevations: List[Elevation]) -> bool:
        """
        return comparison if elevation of (x, y) location on map is in the given Elevation Enum list
        :param x: x int coordinate of game map
        :param y: y int coordinate of game map
        :param elevations: list of Elevation enums
        :return: bool
        """
        return self.terrain[x][y].elevation in elevations
    
    def get_path(self,
                 entity_x: int,
                 entity_y: int,
                 target_x: int,
                 target_y: int,
                 elevations: List[Elevation]
                 ) -> List[Tuple[int, int]]:
        """
        Create a grid of (x, y) coordinates mapping to the (x, y) they came from
        :param entity_x: x int coordinate of this entity on game map
        :param entity_y: y int coordinate of this entity on game map
        :param target_x: x int coordinate of target on game map
        :param target_y: y int coordinate of target on game map
        :param elevations: list of Elevation enums
        :return: dict of tuple (x, y) coordinates -> tuple (x, y) coordinates
        """
        frontier = Queue()
        frontier.put((target_x, target_y))
        came_from = dict()
        came_from[(target_x, target_y)] = (target_x, target_y)
        
        path_found = False
        while not frontier.empty():
            current = frontier.get()
            x, y = current
            for neighbor in self.get_neighbors_at_elevations(x=x, y=y, elevations=elevations):
                if neighbor not in came_from:
                    frontier.put(neighbor)
                    came_from[(neighbor[0], neighbor[1])] = current
                    if neighbor == (entity_x, entity_y):
                        # found a path to target
                        path_found = True
                        break
        if path_found:
            path = []
            current = (entity_x, entity_y)
            while current != (target_x, target_y):
                path.append(current)
                if not current:
                    break
                current = came_from[current]
            path.reverse()
            path.pop()  # remove entity's current hex
            return path
        
        return []
    
    def get_distance_map(self,
                         entity_x: int,
                         entity_y: int,
                         target_x: int,
                         target_y: int,
                         elevations: List[Elevation]
                         ) -> Dict[Tuple[int, int]:int]:
        """
        Create a grid of (x, y) coordinates mapping to the (x, y) they came from
        :param entity_x: x int coordinate of this entity on game map
        :param entity_y: y int coordinate of this entity on game map
        :param target_x: x int coordinate of target on game map
        :param target_y: y int coordinate of target on game map
        :param elevations: list of Elevation enums
        :return: dict of tuple (x, y) coordinates -> tuple (x, y) coordinates
        """
        frontier = Queue()
        frontier.put((target_x, target_y))
        came_from = dict()
        came_from[(target_x, target_y)] = (target_x, target_y)
        
        # lets create the dict, but stop when we've included ALL the neighbors around the target
        #  rather than just when we find the target
        surrounding = self.get_neighbors_at_elevations(x=entity_x, y=entity_y, elevations=elevations)
        
        while not frontier.empty():
            current = frontier.get()
            x, y = current
            for neighbor in self.get_neighbors_at_elevations(x=x, y=y, elevations=elevations):
                if neighbor not in came_from:
                    frontier.put(neighbor)
                    came_from[(neighbor[0], neighbor[1])] = current
                    if neighbor in surrounding:
                        surrounding.remove(neighbor)
                        if len(surrounding) <= 0:
                            with frontier.mutex:
                                frontier.queue.clear()
        # change came_from to distances
        distance_map = {}
        for (x, y) in came_from.keys():
            distance_map[x, y] = get_distance(x, y, target_x, target_y)
        
        return distance_map
    
    def get_neighbors_at_elevations(self, x, y, elevations: List[Elevation]) -> List[Tuple[int, int]]:
        """
        Returns a list of Tuple (x, y) coordinates that are adjacent to given (x, y) coordinates
            if they are contained in the list of valid Elevations
        :param x: x int coordinate of game map
        :param y: y int coordinate of game map
        :param elevations: list of Elevation enums
        :return: list of tuple (x, y) coordinates
        """
        neighbors = []
        for direction in cube_directions:
            start_cube = hex_to_cube(hexagon=Hex(column=x, row=y))
            neighbor_hex = cube_to_hex(cube=cube_add(cube1=start_cube, cube2=direction))
            if self.in_bounds(neighbor_hex.col, neighbor_hex.row) \
                    and self.terrain[neighbor_hex.col][neighbor_hex.row].elevation in elevations:
                neighbors.append((neighbor_hex.col, neighbor_hex.row))
        return neighbors
    
    def get_targets_at_location(self, grid_x: int, grid_y: int) -> List[Optional]:
        """
        Returns a list of Actors at a particular coordinate
        :param grid_x: x int coordinate of game map
        :param grid_y: y int coordinate of game map
        :return: list of Actor
        """
        living_targets = []
        for entity in self.entities:
            if entity.x == grid_x and entity.y == grid_y:
                if entity.is_alive:
                    living_targets.append(entity)
        if self.engine.player in living_targets:
            living_targets.remove(self.engine.player)
        return living_targets
    
    def get_items_at_location(self, grid_x: int, grid_y: int) -> List[Entity]:
        """
        Returns a list of items at a particular coordinate
        :param grid_x: x int coordinate of game map
        :param grid_y: y int coordinate of game map
        :return: list of Entity
        """
        items = []
        for entity in self.entities:
            if entity.x == grid_x and entity.y == grid_y:
                if not entity.is_alive:
                    items.append(entity)
        if self.engine.player in items:
            items.remove(self.engine.player)
        return items
    
    def decoration_damage(self, x: int, y: int, entity: Actor, conditions: Conditions):
        color = colors['pink'] if entity == self.engine.player else colors['mountain']
        # Todo add in damage for cargo: over-weight, over-volume
        if entity.fighter.name == "hull":
            if entity.parent.game_map.terrain[x][y].decoration:
                decoration = self.terrain[x][y].decoration
                damage = 0
                if entity.cargo and entity.cargo.weight > entity.cargo.max_weight:
                    damage += 1
                if decoration in ['rocks']:
                    damage += 2
                    self.engine.message_log.add_message(
                        f"{entity.name} takes {damage} hull damage while trying to dodge rocks", color)
                    entity.fighter.take_damage(damage)
                elif decoration in ['coral']:
                    damage += 1
                    self.engine.message_log.add_message(
                        f"{entity.name} takes {damage} hull damage from scraping coral", color)
                    entity.fighter.take_damage(damage)
                elif decoration in ['sandbar']:
                    if damage > 0:
                        self.engine.message_log.add_message(
                            f"{entity.name} takes {damage} hull damage from bumping sandbar", color)
                        entity.fighter.take_damage(damage)
                crew_loss = 1 if conditions == Conditions.STORMY else 0
                if decoration in ['rocks', 'coral', 'sandbar'] and entity.crew and crew_loss:
                    self.engine.message_log.add_message(
                        f"Man Overboard!", color)
                    entity.crew.take_damage(crew_loss)
        if not entity.flying and entity.parent.game_map.terrain[x][y].decoration:
            if entity.parent.game_map.terrain[x][y].decoration in ['minefield']:
                damage = randint(2, 5)
                if (entity.x, entity.y) in self.engine.player.view.fov:
                    self.engine.message_log.add_message(f"Mines explode!", colors['red'])
                    self.engine.message_log.add_message(
                        f"{entity.name} takes {damage} {entity.fighter.name} damage!", color)
                entity.fighter.take_damage(damage)
                if damage > 3:
                    if (entity.x, entity.y) in self.engine.player.view.fov:
                        self.engine.message_log.add_message(f"Minefield has been cleared")
                    entity.parent.game_map.terrain[x][y].decoration = None
