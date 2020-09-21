from __future__ import annotations

from math import pow
from queue import Queue
from random import randint, random, choice
from typing import List, Tuple
from typing import TYPE_CHECKING

from opensimplex import OpenSimplex

import entity_factory
from game_map import GameMap
from tile import Elevation, Terrain

if TYPE_CHECKING:
    from engine import Engine

ISLAND_GEN = {
    'frequency': 3,
    'rand_pow_x_low': 5,
    'rand_pow_x_high': 10,
    'rand_pow_y_low': 5,
    'rand_pow_y_high': 10,
}

DECORATION_GEN = {
    'frequency': 20,
    'rand_pow_x': 20,
    'rand_pow_y': 20,
    'cutoff': 185,
}


def generate_map(map_width: int, map_height: int, engine: Engine, seed: int) -> GameMap:
    player = engine.player
    
    island_map = GameMap(engine, map_width, map_height, entities=[player])
    
    ev = OpenSimplex(seed=seed)
    island_noise = make_noise_island_map(map_width, map_height, ev, ISLAND_GEN)
    
    ev = OpenSimplex(seed=seed + 1)
    coral_noise = make_noise_list(map_width, map_height, ev, DECORATION_GEN)
    
    ev = OpenSimplex(seed=seed + 2)
    rock_noise = make_noise_list(map_width, map_height, ev, DECORATION_GEN)
    
    ev = OpenSimplex(seed=seed + 3)
    sandbar_noise = make_noise_list(map_width, map_height, ev, DECORATION_GEN)
    
    ev = OpenSimplex(seed=seed + 4)
    seaweed_noise = make_noise_list(map_width, map_height, ev, DECORATION_GEN)
    
    for x in range(map_width):
        for y in range(map_height):
            
            # add mist  TODO: add depending on weather
            mist = True if randint(0, 99) < 10 else False
            
            # decoration
            decoration = None
            if (x, y) in rock_noise:
                decoration = "rocks"
            elif (x, y) in coral_noise:
                decoration = "coral"
            elif (x, y) in sandbar_noise:
                decoration = "sandbar"
            elif (x, y) in seaweed_noise:
                decoration = "seaweed"
            
            if island_noise[x][y] < 100:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.OCEAN,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            elif island_noise[x][y] < 125:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.WATER,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            elif island_noise[x][y] < 150:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.SHALLOWS,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            elif island_noise[x][y] < 160:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.BEACH,
                                                   explored=False,
                                                   mist=mist)
            elif island_noise[x][y] < 170:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.GRASS,
                                                   explored=False,
                                                   mist=mist)
            elif island_noise[x][y] < 200:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.JUNGLE,
                                                   explored=False,
                                                   mist=mist)
            elif island_noise[x][y] < 210:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.MOUNTAIN,
                                                   explored=False,
                                                   mist=mist)
            else:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.VOLCANO,
                                                   explored=False,
                                                   mist=mist)
    ocean = explore_water_iterative(island_map)
    islands = explore_islands(island_map, ocean)
    island = big_island(islands)
    place_port(island_map, island, ocean)
    place_player(island_map, player)
    available_ocean = set(ocean) - player.view.fov
    place_entities(island_map, list(available_ocean))
    return island_map


def place_player(island_map, player):
    player_x = 0
    player_y = 0
    direction = 0
    edge = randint(0, 3)
    if edge == 0:
        player_x = randint(0, island_map.width - 1)
        player_y = 1
        if player_x < island_map.width // 4:
            direction = 2
        elif player_x > 3 * island_map.width // 4:
            direction = 4
        else:
            direction = 3
    elif edge == 1:
        player_x = island_map.width - 2
        player_y = randint(0, island_map.height - 1)
        if player_y < island_map.width // 2:
            direction = 4
        else:
            direction = 5
    elif edge == 2:
        player_x = randint(0, island_map.width - 1)
        player_y = island_map.height - 2
        if player_x < island_map.width // 4:
            direction = 1
        elif player_x > 3 * island_map.width // 4:
            direction = 5
        else:
            direction = 0
    elif edge == 3:
        player_x = 1
        player_y = randint(0, island_map.height - 1)
        if player_y < island_map.width // 2:
            direction = 3
        else:
            direction = 2
    player.place(player_x, player_y, island_map)
    player.facing = direction
    player.view.set_fov()


def explore_islands(island_map, ocean) -> List[List[Tuple[int, int]]]:
    island_list = []
    land_list = []
    for x in range(island_map.width):
        for y in range(island_map.height):
            if (x, y) not in ocean and (x, y) not in land_list:
                island = explore_land_iterative(island_map, x=x, y=y)
                island_list.append(island)
                land_list.extend(island)
    return island_list


def big_island(island_list: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    big_size = 0
    biggest = []
    for island in island_list:
        if len(island) > big_size:
            big_size = len(island)
            biggest = island
    return biggest


def place_port(island_map: GameMap, island, ocean):
    coastline = []
    for (x, y) in island:
        neighbors = island_map.get_neighbors(x, y)
        for neighbor in neighbors:
            if neighbor in ocean:
                coastline.append((x, y))
                break
    (x, y) = choice(coastline)
    island_map.terrain[x][y].decoration = "port"
    island_map.port = (x, y)
    print((x, y))


def make_noise_island_map(map_width, map_height, ev, params):
    frequency = params['frequency']
    rand_pow_x = randint(params['rand_pow_x_low'], params['rand_pow_x_high'])
    rand_pow_y = randint(params['rand_pow_y_low'], params['rand_pow_y_high'])
    
    center_x = (map_width - 1) / 2.0
    center_y = (map_height - 1) / 2.0
    noise_map = []
    for x in range(map_width):
        for y in range(map_height):
            nx = x / map_width - 0.5
            ny = y / map_height - 0.5
            elevation_sum = 0
            i_sum = 0
            for i in range(1, 6):
                p = pow(2, i)
                elevation_sum += noise(ev, p * frequency * nx, p * frequency * ny) / p
                i_sum += 1 / p
            elevation = elevation_sum / i_sum
            x_dist = abs(center_x - x)
            y_dist = abs(center_y - y)
            x_ratio = 1 - pow(x_dist / center_x, rand_pow_x)
            y_ratio = 1 - pow(y_dist / center_y, rand_pow_y)
            ratio = min(x_ratio, y_ratio)
            
            noise_map[x][y] = round(256 * elevation * ratio)
    return noise_map


def make_noise_list(map_width, map_height, ev, params):
    frequency = params['frequency']
    rand_pow_x = params['rand_pow_x']
    rand_pow_y = params['rand_pow_y']
    
    center_x = (map_width - 1) / 2.0
    center_y = (map_height - 1) / 2.0
    noise_list = []
    for x in range(map_width):
        for y in range(map_height):
            nx = x / map_width - 0.5
            ny = y / map_height - 0.5
            elevation_sum = 0
            i_sum = 0
            for i in range(1, 6):
                p = pow(2, i)
                elevation_sum += noise(ev, p * frequency * nx, p * frequency * ny) / p
                i_sum += 1 / p
            elevation = elevation_sum / i_sum
            x_dist = abs(center_x - x)
            y_dist = abs(center_y - y)
            x_ratio = 1 - pow(x_dist / center_x, rand_pow_x)
            y_ratio = 1 - pow(y_dist / center_y, rand_pow_y)
            ratio = min(x_ratio, y_ratio)
            
            if round(256 * elevation * ratio) >= params['cutoff']:
                noise_list.append((x, y))
    
    return noise_list


def noise(gen, nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2d(nx, ny) / 2.0 + 0.5


def place_entities(island_map: GameMap, available):
    for entity in range((island_map.width * island_map.height) // 50):
        # generate monsters here, add to entities list
        (x, y) = choice(available)
        available.remove((x, y))
        rnd = random()
        if rnd < .4:
            turtle = entity_factory.turtle.spawn(island_map, x, y, randint(0, 5))
            turtle.view.set_fov()
        elif rnd < .7:
            bat = entity_factory.bat.spawn(island_map, x, y, randint(0, 5))
            bat.view.set_fov()
        else:
            serpent = entity_factory.serpent.spawn(island_map, x, y, randint(0, 5))
            serpent.view.set_fov()


def explore_water_iterative(game_map: GameMap) -> List[Tuple[int, int]]:
    """
    Finds all connected water from 0, 0
    :param game_map: GameMap
    :return: list of tile coordinates
    """
    x = 0
    y = 0
    frontier = Queue()
    frontier.put((x, y))
    visited = [(x, y)]
    
    while not frontier.empty():
        current = frontier.get()
        x, y = current
        for neighbor in game_map.get_neighbors(x=x, y=y, elevation=Elevation.BEACH):
            if neighbor not in visited:
                frontier.put(neighbor)
                visited.append(neighbor)
    return visited


def explore_land_iterative(game_map: GameMap, x: int, y: int) -> List[Tuple[int, int]]:
    """
    Finds all "islands" on the game map. "islands" are sets of adjacent land tiles. "land tiles" have elevation > 2
    :param game_map: GameMap
    :param x: int x coordinate
    :param y: int y coordinate
    :return: list of tile coordinates
    """
    frontier = Queue()
    frontier.put((x, y))
    visited = [(x, y)]
    
    while not frontier.empty():
        current = frontier.get()
        x, y = current
        for neighbor in game_map.get_neighbors(x=x, y=y, elevation=Elevation.BEACH, below=False):
            if neighbor not in visited:
                frontier.put(neighbor)
                visited.append(neighbor)
    return visited
