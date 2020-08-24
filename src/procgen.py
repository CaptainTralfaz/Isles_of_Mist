from src.game_map import GameMap
from src.tile import Elevation, Terrain


from random import randint, seed
from math import pow
from opensimplex import OpenSimplex


def generate_map(map_width, map_height) -> GameMap:
    island_map = GameMap(map_width, map_height)
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
                island_map.terrain[x][y] = Elevation.OCEAN
            elif height < 125:
                island_map.terrain[x][y] = Elevation.WATER
            elif height < 150:
                island_map.terrain[x][y] = Elevation.SHALLOWS
            elif height < 160:
                island_map.terrain[x][y] = Elevation.BEACH
            elif height < 170:
                island_map.terrain[x][y] = Elevation.GRASS
            elif height < 200:
                island_map.terrain[x][y] = Elevation.JUNGLE
            elif height < 210:
                island_map.terrain[x][y] = Elevation.MOUNTAIN
            else:
                island_map.terrain[x][y] = Elevation.VOLCANO

    return island_map


def noise(gen, nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2d(nx, ny) / 2.0 + 0.5
