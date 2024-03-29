from __future__ import annotations

from math import pow
from queue import Queue
from random import randint, random, choice
from typing import List, Tuple
from typing import TYPE_CHECKING

from opensimplex import OpenSimplex

import entity_factory
from components.cargo import Cargo
from constants.constants import move_elevations
from constants.enums import Elevation
from game_map import GameMap
from tile import Terrain
from weather import Weather

if TYPE_CHECKING:
    from engine import Engine
    from ui import DisplayInfo

ISLAND_GEN = {
    'frequency': 3,
    'rand_pow_x_low': 8,
    'rand_pow_x_high': 10,
    'rand_pow_y_low': 8,
    'rand_pow_y_high': 10,
}

DECORATION_GEN = {
    'frequency': 20,
    'rand_pow_x': 25,
    'rand_pow_y': 25,
    'cutoff': 185,
}

ELEVATION_LEVEL = {
    'ocean': 100,
    'water': 125,
    'shallows': 150,
    'beach': 160,
    'grass': 170,
    'jungle': 200,
    'mountain': 255,
}


def generate_map(map_width: int, map_height: int, engine: Engine, seed: int, ui_layout: DisplayInfo) -> GameMap:
    player = engine.player
    
    island_map = GameMap(width=map_width, height=map_height, engine=engine, entities=[player])
    island_map.weather = Weather(ui_layout.viewport_width, ui_layout.viewport_height, island_map)
    
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
            
            # add mist
            mist_chance = island_map.weather.get_weather_info['mist'] \
                          + engine.time.get_time_of_day_info['mist']
            mist = True if randint(0, 99) < mist_chance else False
            
            # decoration
            decoration = None
            if island_noise[x][y] < ELEVATION_LEVEL['shallows']:
                if (x, y) in rock_noise:
                    decoration = "rocks"
                elif (x, y) in coral_noise:
                    decoration = "coral"
                elif (x, y) in sandbar_noise:
                    decoration = "sandbar"
                elif (x, y) in seaweed_noise:
                    decoration = "seaweed"
            elif island_noise[x][y] < ELEVATION_LEVEL['beach']:
                if (x, y) in rock_noise:
                    decoration = "quarry"
                elif (x, y) in coral_noise:
                    decoration = "claypool"  # clay pit
                elif (x, y) in sandbar_noise:
                    decoration = "tidepool"
                elif (x, y) in seaweed_noise:
                    decoration = "tidepool"
            elif island_noise[x][y] < ELEVATION_LEVEL['grass']:
                if (x, y) in rock_noise:
                    decoration = "quarry"
                elif (x, y) in coral_noise:
                    decoration = "claypool"  # clay pit
                elif (x, y) in sandbar_noise:
                    decoration = "farmland"
                elif (x, y) in seaweed_noise:
                    decoration = "farmland"
            elif island_noise[x][y] < ELEVATION_LEVEL['jungle']:
                if (x, y) in rock_noise:
                    decoration = "mine"
                elif (x, y) in coral_noise:
                    decoration = "claypool"
                elif (x, y) in sandbar_noise:
                    decoration = "swamp"
                elif (x, y) in seaweed_noise:
                    decoration = "swamp"
            elif island_noise[x][y] < ELEVATION_LEVEL['mountain']:
                if (x, y) in rock_noise:
                    decoration = "mine"
                elif (x, y) in coral_noise:
                    decoration = "mine"
                elif (x, y) in sandbar_noise:
                    decoration = "volcano"
                elif (x, y) in seaweed_noise:
                    decoration = "volcano"
            
            if island_noise[x][y] < ELEVATION_LEVEL['ocean']:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.OCEAN,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            elif island_noise[x][y] < ELEVATION_LEVEL['water']:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.WATER,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            elif island_noise[x][y] < ELEVATION_LEVEL['shallows']:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.SHALLOWS,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            elif island_noise[x][y] < ELEVATION_LEVEL['beach']:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.BEACH,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            elif island_noise[x][y] < ELEVATION_LEVEL['grass']:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.GRASS,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            elif island_noise[x][y] < ELEVATION_LEVEL['jungle']:
                island_map.terrain[x][y] = Terrain(elevation=Elevation.JUNGLE,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)
            else:  # ELEVATION_LEVEL['mountain']
                island_map.terrain[x][y] = Terrain(elevation=Elevation.MOUNTAIN,
                                                   explored=False,
                                                   decoration=decoration,
                                                   mist=mist)

    ocean = explore_water_iterative(island_map)
    islands = explore_islands(island_map, ocean)
    island = big_island(islands)
    place_port(island_map, island, ocean)
    place_player(island_map, player)
    
    elevations = elevation_choices(island_map, player.view.fov)
    place_entities(island_map, elevations)
    return island_map


def place_player(island_map, player):
    player_x = 0
    player_y = 0
    direction = 0
    edge = randint(0, 3)
    if edge == 0:
        player_x = randint(1, island_map.width - 2)
        player_y = 1
        if player_x < island_map.width // 4:
            direction = 2
        elif player_x > 3 * island_map.width // 4:
            direction = 4
        else:
            direction = 3
    elif edge == 1:
        player_x = island_map.width - 2
        player_y = randint(1, island_map.height - 2)
        if player_y < island_map.width // 2:
            direction = 4
        else:
            direction = 5
    elif edge == 2:
        player_x = randint(1, island_map.width - 2)
        player_y = island_map.height - 2
        if player_x < island_map.width // 4:
            direction = 1
        elif player_x > 3 * island_map.width // 4:
            direction = 5
        else:
            direction = 0
    elif edge == 3:
        player_x = 1
        player_y = randint(1, island_map.height - 2)
        if player_y < island_map.width // 2:
            direction = 2
        else:
            direction = 1
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
        neighbors = island_map.get_neighbors_at_elevations(x, y, elevations='water')
        coast = False
        for neighbor in neighbors:
            if neighbor in ocean:
                coast = True
        if coast:
            coastline.append((x, y))
    (x, y) = choice(coastline)
    island_map.terrain[x][y].decoration = "port"
    island_map.port.location = (x, y)
    print((x, y))


def make_noise_island_map(map_width, map_height, ev, params):
    frequency = params['frequency']
    rand_pow_x = randint(params['rand_pow_x_low'], params['rand_pow_x_high'])
    rand_pow_y = randint(params['rand_pow_y_low'], params['rand_pow_y_high'])
    
    center_x = (map_width - 1) / 2.0
    center_y = (map_height - 1) / 2.0
    noise_map = [[0 for y in range(map_height)] for x in range(map_width)]
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


def place_entities(island_map: GameMap, elevations):
    for entity in range((island_map.width * island_map.height) // 50):
        # generate monsters here, add to entities list
        rnd = random()
        if rnd < .3:
            available = []
            for elevation in move_elevations['water']:
                available.extend(elevations[elevation.name])
            (x, y) = choice(available)
            turtle = entity_factory.turtle.spawn(island_map, x, y, randint(0, 5))
            turtle.view.set_fov()
            turtle.cargo = Cargo(max_volume=20, max_weight=20, manifest=get_entity_manifest('turtle'))
        elif rnd < .5:
            available = []
            for elevation in move_elevations['fly']:
                available.extend(elevations[elevation.name])
            (x, y) = choice(available)
            bat = entity_factory.bat.spawn(island_map, x, y, randint(0, 5))
            bat.view.set_fov()
            bat.cargo = Cargo(max_volume=5, max_weight=5, manifest=get_entity_manifest('bat'))
        elif rnd < .7:
            available = []
            for elevation in move_elevations['shore']:
                available.extend(elevations[elevation.name])
            (x, y) = choice(available)
            mermaid = entity_factory.mermaid.spawn(island_map, x, y, randint(0, 5))
            mermaid.view.set_fov()
            mermaid.cargo = Cargo(max_volume=5, max_weight=5, manifest=get_entity_manifest('mermaid'))
        elif rnd < .9:
            available = []
            for elevation in move_elevations['deep_water']:
                available.extend(elevations[elevation.name])
            (x, y) = choice(available)
            serpent = entity_factory.serpent.spawn(island_map, x, y, randint(0, 5))
            serpent.view.set_fov()
            serpent.cargo = Cargo(max_volume=10, max_weight=10, manifest=get_entity_manifest('serpent'))
        elif rnd < .97:
            available = []
            for elevation in move_elevations['shallows']:
                available.extend(elevations[elevation.name])
            (x, y) = choice(available)
            shipwreck = entity_factory.shipwreck.spawn(island_map, x, y)
            shipwreck.cargo = Cargo(max_volume=20, max_weight=20, manifest=get_entity_manifest('shipwreck'))
        elif rnd < .98:
            available = []
            for elevation in move_elevations['ocean']:
                available.extend(elevations[elevation.name])
            (x, y) = choice(available)
            chest = entity_factory.chest.spawn(island_map, x, y)
            manifest = get_entity_manifest('chest')
            coins = 0
            if 'coins' in manifest.keys():
                coins = manifest['coins']
                del (manifest['coins'])
            chest.cargo = Cargo(max_volume=10, max_weight=10, manifest=manifest, coins=coins)
        else:
            available = []
            for elevation in move_elevations['water']:
                available.extend(elevations[elevation.name])
            (x, y) = choice(available)
            bottle = entity_factory.bottle.spawn(island_map, x, y)
            bottle.cargo = Cargo(max_volume=2, max_weight=2, manifest=get_entity_manifest('bottle'))


def elevation_choices(game_map: GameMap, player_fov) -> dict:
    elevations = {}
    for key in Elevation:
        elevations[key.name] = []
    for x in range(game_map.width):
        for y in range(game_map.height):
            elevations[game_map.terrain[x][y].elevation.name].append((x, y))
    for key in Elevation:
        for (x, y) in player_fov:
            if (x, y) in elevations[key.name]:
                elevations[key.name].remove((x, y))
    return elevations


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
        for neighbor in game_map.get_neighbors_at_elevations(x=x, y=y, elevations='water'):
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
        for neighbor in game_map.get_neighbors_at_elevations(x=x, y=y, elevations='land'):
            if neighbor not in visited:
                frontier.put(neighbor)
                visited.append(neighbor)
    return visited


def get_entity_manifest(entity):
    if entity == "serpent":
        meat = randint(1, 2)
        scales = randint(0, 1)
        manifest = {'meat': meat}
        if scales:
            manifest['scale'] = scales
        return manifest
    elif entity == "bat":
        meat = 1
        bat_wing = randint(0, 2)
        manifest = {'meat': meat}
        if bat_wing:
            manifest['bat wing'] = bat_wing
        return manifest
    elif entity == "turtle":
        meat = randint(4, 8)
        shell = randint(0, 1)
        manifest = {'meat': meat}
        if shell:
            manifest['shell'] = shell
        return manifest
    elif entity == "mermaid":
        fish = randint(0, 2)
        pearl = randint(0, 1)
        manifest = {}
        if fish:
            manifest['fish'] = fish
        if pearl:
            manifest['pearl'] = pearl
        return manifest
    elif entity == 'chest':
        coins = randint(50, 100)
        arrows = randint(10, 30)
        if randint(0, 1):
            tar = randint(3, 5)
            rope = randint(3, 5)
            return {'coins': coins,
                    'arrows': arrows,
                    'tar': tar,
                    'rope': rope}
        else:
            fruit = randint(4, 9)
            rum = randint(2, 5)
            return {'coins': coins,
                    'arrows': arrows,
                    'fruit': fruit,
                    'rum': rum}
    elif entity == 'bottle':
        return {('message' if randint(0, 1) else 'map'): 1}
    elif entity == 'shipwreck':
        canvas = randint(3, 5)
        wood = randint(4, 8)
        bolts = randint(3, 6)
        cannonballs = randint(2, 5)
        mines = randint(0, 2)
        manifest = {'canvas': canvas,
                    'wood': wood,
                    'bolts': bolts,
                    'cannonballs': cannonballs}
        if mines:
            manifest['mines'] = mines
        return manifest
