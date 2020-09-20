from random import randint

from game_map import GameMap
from utilities import direction_angle, get_neighbor


class Weather:
    def __init__(self, wind_direction: int = None):
        if wind_direction is not None:
            self.wind_direction = wind_direction
        else:
            self.wind_direction = randint(0, 5)
        print(f"wind direction: {self.wind_direction}")
        
    def change_wind(self, rotate: int):
        self.wind_direction += rotate
        if self.wind_direction >= len(direction_angle):
            self.wind_direction = 0
        elif self.wind_direction < 0:
            self.wind_direction = len(direction_angle) - 1
            
    def roll_mist(self, game_map: GameMap):
        new_mist = []
        for x in range(game_map.width):
            for y in range(game_map.height):
                if game_map.terrain[x][y].mist:
                    new_mist.append(get_neighbor(x, y, self.wind_direction))
                game_map.terrain[x][y].mist = False
        # add new mist at edges:
        bottom = True if self.wind_direction in [0, 1, 5] else False
        left = True if self.wind_direction in [1, 2] else False
        top = True if self.wind_direction in [2, 3, 4] else False
        right = True if self.wind_direction in [4, 5] else False
        
        mist_chance = 10
        
        if top:
            for x in range(game_map.width):
                mist = True if randint(0, 99) < mist_chance else False
                if mist:
                    new_mist.append((x, 0))
        if right:
            for y in range(game_map.height):
                mist = True if randint(0, 99) < mist_chance else False
                if mist:
                    new_mist.append((game_map.width - 1, y))
        if bottom:
            for x in range(game_map.width):
                mist = True if randint(0, 99) < mist_chance else False
                if mist:
                    new_mist.append((x, game_map.height - 1))
        if left:
            for y in range(game_map.height):
                mist = True if randint(0, 99) < mist_chance else False
                if mist:
                    new_mist.append((0, y))
                    
        # add new fog to terrain
        for x, y in new_mist:
            if game_map.in_bounds(x, y):
                game_map.terrain[x][y].mist = True
