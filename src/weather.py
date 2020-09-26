from enum import Enum, auto
from random import randint

from constants import colors
from game_map import GameMap
from utilities import direction_angle, get_neighbor


class Conditions(Enum):
    """
    Enum of possible weather values
    """
    CLEAR = auto()
    HAZY = auto()
    CLOUDY = auto()
    RAINY = auto()
    STORMY = auto()


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
    def __init__(self, parent, wind_direction: int = None, conditions: Conditions = None):
        self.wind_direction = randint(0, 5) if wind_direction is None else wind_direction
        self.conditions = Conditions(randint(1, 3)) if conditions is None else conditions
        self.wind_count = 0
        self.wind_min_count = 25
        self.conditions_count = 0
        self.conditions_min_count = 50
        self.engine = parent
    
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
                        self.engine.message_log.add_message(f"Wind dies down", text_color=colors['grass'])
                else:
                    if self.wind_direction is None:
                        self.wind_count = 0
                        self.wind_direction = randint(0, 5)
                        self.engine.message_log.add_message(f"Wind starts blowing {wind_dir[self.wind_direction]}",
                                                            text_color=colors['grass'])
                    else:
                        self.wind_count = 0
                        self.rotate_wind(change)
                        self.engine.message_log.add_message(f"Wind rotates to the {wind_dir[self.wind_direction]}",
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
                self.engine.message_log.add_message(text, text_color=colors['grass'])
    
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
        
        tod_mist = self.engine.time.get_time_of_day_info['mist']
        weather_mist = weather_effects[self.engine.weather.conditions]['mist']
        mist_chance = tod_mist + weather_mist
        
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


class Time:
    def __init__(self, hrs=9, mins=00, day=1, month=1, year=1111):
        """
        Object holding game time information
        12 months per year, 30 days per month, 24 hrs per day, 60 minutes per hour

        """
        self.hrs = hrs
        self.mins = mins
        self.day = day
        self.month = month
        self.year = year  # Year of Steve
    
    def to_json(self):
        """
        json serialized Time class
        :return: json representation of Time
        """
        return {
            'hrs': self.hrs,
            'mins': self.mins,
            'day': self.day,
            'month': self.month,
            'year': self.year,
        }
    
    @staticmethod
    def from_json(json_data):
        hrs = json_data.get('hrs')
        mins = json_data.get('mins')
        day = json_data.get('day')
        month = json_data.get('month')
        year = json_data.get('year')
        
        return Time(hrs=hrs, mins=mins, day=day, month=month, year=year)
    
    def roll_min(self, amount) -> None:
        """
        add minutes to the time ticker
        :return: None
        """
        total = self.mins + amount
        if self.mins >= 60:
            self.mins = total - 60
            self.roll_hrs(1)
        else:
            self.mins = total
    
    def roll_hrs(self, amount):
        total = self.hrs + amount
        if total > 23:
            self.hrs = total - 24
            self.roll_day(1)
        else:
            self.hrs = total
    
    def roll_day(self, amount):
        total = self.day + amount
        if total > 30:
            self.day = total - 30
            self.roll_month(1)
        else:
            self.day = total
    
    def roll_month(self, amount):
        total = self.month + amount
        if self.month > 12:
            self.month = total - 12
            self.roll_year(1)
        else:
            self.month = total
    
    def roll_year(self, amount):
        total = self.year + amount
        if total > 1111:
            print("out of turns!")
    
    @property
    def get_sky_color(self):
        day = 1440  # minutes in a day
        half_day = 1440 // 2  # half day
        time_shift = abs(self.hrs * 60 + self.mins - half_day)  # 0 -> 720 -> 0
        r_period = 2
        r = 2 * abs(day // 12 - r_period * abs((time_shift // 6) - day // (12 * r_period)))
        g = (half_day - time_shift) // 3
        if g > 125:
            g = 125
        b = half_day - time_shift
        if b > 225:
            b = 225
        return r, g, b
    
    @property
    def get_time_of_day_info(self):
        """
        Gets info for each particular time of day
        :return: dict of information pertaining to the particular time of day
        """
        if self.hrs in [1, 2]:
            return time_of_day_info[TimeOfDay.DEEP_NIGHT]
        elif self.hrs in [3, 4]:
            return time_of_day_info[TimeOfDay.WEE_HOURS]
        elif self.hrs in [5, 6]:
            return time_of_day_info[TimeOfDay.DAWN]
        elif self.hrs in [7, 8]:
            return time_of_day_info[TimeOfDay.MORNING]
        elif self.hrs in [9, 10]:
            return time_of_day_info[TimeOfDay.FORENOON]
        elif self.hrs in [11, 12]:
            return time_of_day_info[TimeOfDay.NOON]
        elif self.hrs in [13, 14]:
            return time_of_day_info[TimeOfDay.AFTERNOON]
        elif self.hrs in [15, 16]:
            return time_of_day_info[TimeOfDay.LATE_DAY]
        elif self.hrs in [17, 18]:
            return time_of_day_info[TimeOfDay.EVENING]
        elif self.hrs in [19, 20]:
            return time_of_day_info[TimeOfDay.TWILIGHT]
        elif self.hrs in [21, 22]:
            return time_of_day_info[TimeOfDay.NIGHT]
        elif self.hrs in [23, 0]:
            return time_of_day_info[TimeOfDay.MIDNIGHT]
        else:
            return KeyError


class TimeOfDay(Enum):
    """
    Time of Day Enum, mainly used as key for information dictionary
    """
    DAWN = auto()
    MORNING = auto()
    FORENOON = auto()
    NOON = auto()
    AFTERNOON = auto()
    LATE_DAY = auto()
    EVENING = auto()
    TWILIGHT = auto()
    NIGHT = auto()
    MIDNIGHT = auto()
    DEEP_NIGHT = auto()
    WEE_HOURS = auto()


time_of_day_info = {TimeOfDay.DAWN: {'name': 'Dawn', 'begin': 5, 'view': 0, 'mist': 10},
                    TimeOfDay.MORNING: {'name': 'Morning', 'begin': 7, 'view': 0, 'mist': 5},
                    TimeOfDay.FORENOON: {'name': 'Forenoon', 'begin': 9, 'view': 0, 'mist': 0},
                    TimeOfDay.NOON: {'name': 'Noontime', 'begin': 11, 'view': 0, 'mist': 0},
                    TimeOfDay.AFTERNOON: {'name': 'Afternoon', 'begin': 13, 'view': 0, 'mist': 0},
                    TimeOfDay.LATE_DAY: {'name': 'Late Day', 'begin': 15, 'view': 0, 'mist': 0},
                    TimeOfDay.EVENING: {'name': 'Evening', 'begin': 17, 'view': 0, 'mist': 0},
                    TimeOfDay.TWILIGHT: {'name': 'Twilight', 'begin': 19, 'view': 0, 'mist': 0},
                    TimeOfDay.NIGHT: {'name': 'Night', 'begin': 21, 'view': -1, 'mist': 0},
                    TimeOfDay.MIDNIGHT: {'name': 'Midnight', 'begin': 23, 'view': -2, 'mist': 5},
                    TimeOfDay.DEEP_NIGHT: {'name': 'Deep Night', 'begin': 1, 'view': -2, 'mist': 10},
                    TimeOfDay.WEE_HOURS: {'name': 'Wee Hours', 'begin': 3, 'view': -1, 'mist': 15}
                    }
