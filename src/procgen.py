from __future__ import annotations

from math import pow
from queue import Queue
from random import randint, random, choice
from typing import List, Tuple
from typing import TYPE_CHECKING

from opensimplex import OpenSimplex

import entity_factory
from game_map import GameMap, get_hex_water_neighbors
from tile import Elevation, tile_size, Terrain

if TYPE_CHECKING:
    from engine import Engine


def generate_map(map_width: int, map_height: int, engine: Engine) -> GameMap:
    player = engine.player
    
    island_map = GameMap(engine, map_width, map_height, entities=[player])
    # noise_map = [[0.0 for y in range(map_height)] for x in range(map_width)]
    
    center_x = (map_width - 1) / 2.0
    center_y = (map_height - 1) / 2.0
    
    sd = randint(0, 10000)
    gen = OpenSimplex(seed=sd)
    frequency = 3  # randint(2, 4)
    rand_pow_x = randint(5, 10)
    rand_pow_y = randint(5, 10)
    print(sd, frequency, rand_pow_x, rand_pow_y)
    
    for x in range(map_width):
        for y in range(map_height):
            nx = x / map_width - 0.5
            ny = y / map_height - 0.5
            elevation_sum = 0
            i_sum = 0
            for i in range(1, 6):
                p = pow(2, i)
                elevation_sum += noise(gen, p * frequency * nx, p * frequency * ny) / p
                i_sum += 1 / p
            elevation = elevation_sum / i_sum
            x_dist = abs(center_x - x)
            y_dist = abs(center_y - y)
            x_ratio = 1 - pow(x_dist / center_x, rand_pow_x)
            y_ratio = 1 - pow(y_dist / center_y, rand_pow_y)
            ratio = min(x_ratio, y_ratio)
            
            # noise_map[x][y] = ratio
            
            height = round(256 * elevation * ratio)
            if height < 100:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.OCEAN, explored=True)
            elif height < 125:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.WATER, explored=True)
            elif height < 150:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.SHALLOWS, explored=True)
            elif height < 160:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.BEACH, explored=True)
            elif height < 170:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.GRASS, explored=True)
            elif height < 200:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.JUNGLE, explored=True)
            elif height < 210:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.MOUNTAIN, explored=True)
            else:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.VOLCANO, explored=True)
    
    player_x, player_y = place_entities(island_map)
    player.place(player_x * tile_size, player_y * tile_size, island_map)
    
    return island_map


def noise(gen, nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2d(nx, ny) / 2.0 + 0.5


def place_entities(island_map: GameMap) -> Tuple[int, int]:
    water = explore_water_iterative(island_map, 0, 0)
    
    for entity in range((island_map.width * island_map.height) // 50):
        water_tile = choice(water)
        water.remove(water_tile)
        # generate monsters here, add to entities list
        rnd = random()
        if rnd < .4:
            entity_factory.turtle.spawn(island_map, water_tile[0] * tile_size, water_tile[1] * tile_size, randint(0, 5))
        elif rnd < .7:
            entity_factory.bat.spawn(island_map, water_tile[0] * tile_size, water_tile[1] * tile_size, randint(0, 5))
        else:
            entity_factory.serpent.spawn(island_map, water_tile[0] * tile_size, water_tile[1] * tile_size,
                                         randint(0, 5))
    return choice(water)


def explore_water_iterative(game_map: GameMap, x: int, y: int) -> List[Tuple[int, int]]:
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
        for neighbor in get_hex_water_neighbors(game_map=game_map, x=x, y=y):
            if neighbor not in visited:
                frontier.put(neighbor)
                visited.append(neighbor)
    return visited
