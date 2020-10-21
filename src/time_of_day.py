from pygame import Surface

from constants.enums import TimeOfDay


class Time:
    def __init__(self, hrs=9, mins=0, day=1, month=1, year=1111):  # Year of Steve
        """
        Object holding game time information
        12 months per year, 30 days per month, 24 hrs per day, 60 minutes per hour

        """
        self.hrs = hrs
        self.mins = mins
        self.day = day
        self.month = month
        self.year = year
        self.parent = None
    
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
        if total >= 60:
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
        if total > 12:
            self.month = total - 12
            self.roll_year(1)
        else:
            self.month = total
        self.parent.player.crew.pay_crew()
    
    def roll_year(self, amount):
        total = self.year + amount
        if total > 1111:
            print("out of turns!")
    
    def tint_render(self, panel):
        tint_surf = Surface((panel.get_width(), panel.get_height()))
        tint_surf.set_alpha(abs(self.hrs * 60 + self.mins - 720) // 6)
        tint = self.get_sky_color
        tint_surf.fill(tint)
        panel.blit(tint_surf, (0, 0))
    
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


time_of_day_info = {TimeOfDay.DAWN: {'name': 'Dawn', 'begin': 5, 'view': 0, 'mist': 10},
                    TimeOfDay.MORNING: {'name': 'Morning', 'begin': 7, 'view': 0, 'mist': 5},
                    TimeOfDay.FORENOON: {'name': 'Forenoon', 'begin': 9, 'view': 0, 'mist': 0},
                    TimeOfDay.NOON: {'name': 'Noontime', 'begin': 11, 'view': 0, 'mist': 0},
                    TimeOfDay.AFTERNOON: {'name': 'Afternoon', 'begin': 13, 'view': 0, 'mist': 0},
                    TimeOfDay.LATE_DAY: {'name': 'Late Day', 'begin': 15, 'view': 0, 'mist': 0},
                    TimeOfDay.EVENING: {'name': 'Evening', 'begin': 17, 'view': 0, 'mist': 0},
                    TimeOfDay.TWILIGHT: {'name': 'Twilight', 'begin': 19, 'view': 0, 'mist': 5},
                    TimeOfDay.NIGHT: {'name': 'Night', 'begin': 21, 'view': -1, 'mist': 10},
                    TimeOfDay.MIDNIGHT: {'name': 'Midnight', 'begin': 23, 'view': -2, 'mist': 15},
                    TimeOfDay.DEEP_NIGHT: {'name': 'Deep Night', 'begin': 1, 'view': -2, 'mist': 20},
                    TimeOfDay.WEE_HOURS: {'name': 'Wee Hours', 'begin': 3, 'view': -1, 'mist': 15}
                    }
