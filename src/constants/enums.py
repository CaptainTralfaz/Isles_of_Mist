from enum import Enum, auto


class Conditions(Enum):
    """
    Enum of possible weather values
    """
    CLEAR = auto()
    HAZY = auto()
    CLOUDY = auto()
    RAINY = auto()
    STORMY = auto()


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


class GameStates(Enum):
    """
    Enum of possible game states
    """
    ACTION = auto()
    MAIN_MENU = auto()
    WEAPON_CONFIG = auto()
    CREW_CONFIG = auto()
    CARGO_CONFIG = auto()
    MERCHANT = auto()
    TAVERN = auto()
    SMITHY = auto()
    UPGRADES = auto()
    PLAYER_DEAD = auto()


class MenuKeys(Enum):
    """
    Enum of possible menu keys
    """
    UP = auto()
    RIGHT = auto()
    LEFT = auto()
    DOWN = auto()


class ShipConfig(Enum):
    """
    Enum of possible menu keys
    """
    SAILS = auto()
    CARGO = auto()
    CREW = auto()
    WEAPONS = auto()


class KeyMod(Enum):
    """
    Enum of possible weather values
    """
    SHIFT = auto()
    COMMAND = auto()
    OPTION = auto()


class ItemType(Enum):
    """
    Enum of possible Item Types
    """
    MONEY = auto()
    AMMO = auto()
    SUPPLIES = auto()
    GOODS = auto()
    MATERIALS = auto()
    EXOTICS = auto()
    WEAPON = auto()


class Location(Enum):
    """
    Enum of attack directions
    """
    FORE = auto()
    STARBOARD = auto()
    PORT = auto()
    AFT = auto()
    STORAGE = auto()


class PortVisit(Enum):
    """
    Enum of attack directions
    """
    SHIPYARD = auto()
    MERCHANT = auto()
    TAVERN = auto()
    SMITHY = auto()


class RenderOrder(Enum):
    """
    Enum of render order
    """
    CORPSE = auto()
    FLOATER = auto()
    SWIMMER = auto()
    PLAYER = auto()
    FLYER = auto()


class Elevation(Enum):
    """
    Enum to track elevation
    """
    OCEAN = auto()
    WATER = auto()
    SHALLOWS = auto()
    BEACH = auto()
    GRASS = auto()
    JUNGLE = auto()
    MOUNTAIN = auto()
    ALL = ()
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    
    def __ne__(self, other):
        if self.__class__ is other.__class__:
            return self.value != other.value
        return NotImplemented
