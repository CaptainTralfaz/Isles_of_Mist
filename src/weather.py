from __future__ import annotations

from random import randint, choice
from typing import TYPE_CHECKING

from pygame import draw, Surface

from constants.colors import colors
from constants.constants import margin, wind_min_count, conditions_min_count
from constants.enums import Conditions
from utilities import direction_angle, get_neighbor

if TYPE_CHECKING:
    from game_map import GameMap

weather_effects = {
    Conditions.CLEAR: {'name': 'clear', 'view': 1, 'mist': 0},
    Conditions.HAZY: {'name': 'hazy', 'view': 0, 'mist': 5},
    Conditions.CLOUDY: {'name': 'cloudy', 'view': 0, 'mist': 10},
    Conditions.RAINY: {'name': 'rainy', 'view': -1, 'mist': 15},
    Conditions.STORMY: {'name': 'stormy', 'view': -2, 'mist': 20},
}

wind_dir = {
    0: "north",
    1: "northeast",
    2: "southeast",
    3: "south",
    4: "southwest",
    5: "northwest",
}


class Weather:
    def __init__(self,
                 parent: GameMap,
                 width: int,
                 height: int,
                 wind_direction: int = None,
                 conditions: Conditions = None,
                 wind_count: int = 0,
                 conditions_count: int = 0):
        self.wind_direction = randint(0, 5) if wind_direction is None else wind_direction
        self.conditions = Conditions(randint(2, 3)) if conditions is None else conditions
        self.wind_count = wind_count
        self.wind_min_count = wind_min_count
        self.conditions_count = conditions_count
        self.conditions_min_count = conditions_min_count
        self.game_map = parent
        self.rain = Rain(width, height)
        
    @property
    def get_weather_info(self):
        """
        Returns weather effects dictionary depending on the conditions
        :return: dict of weather effects
        """
        if self.conditions == Conditions.CLEAR:
            return weather_effects[Conditions.CLEAR]
        elif self.conditions == Conditions.HAZY:
            return weather_effects[Conditions.HAZY]
        elif self.conditions == Conditions.CLOUDY:
            return weather_effects[Conditions.CLOUDY]
        elif self.conditions == Conditions.RAINY:
            return weather_effects[Conditions.RAINY]
        elif self.conditions == Conditions.STORMY:
            return weather_effects[Conditions.STORMY]
    
    def to_json(self):
        return {
            'wind_direction': self.wind_direction,
            'wind_count': self.wind_count,
            'conditions': self.conditions.value,
            'conditions_count': self.conditions_count,
        }
    
    def roll_wind(self):
        self.wind_count += 1
        if self.wind_count > self.wind_min_count:
            if randint(0, 99) < self.wind_count:
                change = randint(-1, 1)
                if change == 0:
                    if self.wind_direction is None:
                        return
                    else:
                        self.wind_count = 0
                        self.wind_direction = None
                        self.game_map.engine.message_log.add_message(
                            f"Wind dies down",
                            text_color=colors['grass'])
                else:
                    if self.wind_direction is None:
                        self.wind_count = 0
                        self.wind_direction = randint(0, 5)
                        self.game_map.engine.message_log.add_message(
                            f"Wind starts blowing {wind_dir[self.wind_direction]}",
                            text_color=colors['grass'])
                    else:
                        self.wind_count = 0
                        self.rotate_wind(change)
                        self.game_map.engine.message_log.add_message(
                            f"Wind rotates to the {wind_dir[self.wind_direction]}",
                            text_color=colors['grass'])
    
    def rotate_wind(self, rotate: int):
        self.wind_direction += rotate
        if self.wind_direction >= len(direction_angle):
            self.wind_direction = 0
        elif self.wind_direction < 0:
            self.wind_direction = len(direction_angle) - 1
    
    def roll_weather(self):
        self.conditions_count += 1
        if self.conditions_count > self.conditions_min_count:
            if randint(0, 199) < self.conditions_count:
                change = randint(0, 2)
                if change:  # weather gets better
                    if self.conditions.value == 1:  # can't get any better
                        return
                    else:
                        self.conditions_count = 0
                        self.conditions = Conditions(self.conditions.value - 1)
                else:  # weather gets worse
                    if self.conditions.value == 5:  # can't get any worse
                        self.conditions_count += 1  # don't want storms lasting too long
                    else:
                        self.conditions_count = 0
                        self.conditions = Conditions(self.conditions.value + 1)
                text = f"The weather becomes {self.conditions.name.lower().capitalize()}"
                self.game_map.engine.message_log.add_message(text, text_color=colors['grass'])
    
    def roll_mist(self, game_map: GameMap):
        new_mist = []
        tod_mist = self.game_map.engine.time.get_time_of_day_info['mist']
        weather_mist = weather_effects[self.game_map.weather.conditions]['mist']
        mist_chance = tod_mist + weather_mist
        
        if self.wind_direction is not None:
            # move mist with wind
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
        else:
            # else collect mist without moving
            for x in range(game_map.width):
                for y in range(game_map.height):
                    if game_map.terrain[x][y].mist:
                        new_mist.append((x, y))
                    game_map.terrain[x][y].mist = False
        
        # adjust mist toward current %
        mist_target = mist_chance * 100
        mist_actual = (len(new_mist) * 10000) // (game_map.width * game_map.height)
        mist_change = abs((mist_target - mist_actual) // 10)
        if mist_target > mist_actual:
            for i in range(mist_change):  # might hit a tile with mist already, but who cares?
                pick_x = randint(0, game_map.width - 1)
                pick_y = randint(0, game_map.width - 1)
                if (pick_x, pick_y) not in new_mist:
                    new_mist.append((pick_x, pick_y))
            # print(f"{mist_target} > {mist_actual}: added {mist_change} mist")
        else:
            for i in range(mist_change):
                pick = choice(new_mist)
                new_mist.remove(pick)
            # print(f"{mist_target} > {mist_actual}: removed {mist_change} mist")
        
        # add new fog to terrain
        for x, y in new_mist:
            if game_map.in_bounds(x, y):
                game_map.terrain[x][y].mist = True


class Rain:
    def __init__(self, view_width, view_height):
        self.width = view_width - 2 * margin
        self.height = view_height - 2 * margin
        self.locations = self.gen_locations()
    
    # Loop 50 times and add an object in a random x,y position
    def gen_locations(self):
        locations = []
        for i in range(100):
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            s = randint(10, 20)
            locations.append((x, y, s))
        return locations
    
    def render(self, console, conditions):
        rain_surf = Surface((console.get_width(), console.get_height()))
        rain_surf.fill(colors['dk_gray'])
        if conditions == Conditions.RAINY:
            alpha = 50
        elif conditions == Conditions.STORMY:
            if randint(0, 100) == 0:
                alpha = 255
                rain_surf.fill(colors['lt_gray'])
            else:
                alpha = 80
        else:
            alpha = 0
        rain_surf.set_alpha(alpha)
        
        new_loc = []
        for x, y, s in self.locations:
            # Draw the line
            draw.line(rain_surf, colors['white'], (x, y), (x, y - s), 1)
            # reset if past bottom of viewport
            if y + s > self.height:
                x = randint(0, self.width - 1)
                y = 0
                s = randint(10, 20)
            new_loc.append((x, y + s, s))
        self.locations = new_loc
        console.blit(rain_surf, (0, 0))
