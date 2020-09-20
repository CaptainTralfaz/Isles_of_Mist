from enum import auto, Enum


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
    VOLCANO = auto()
    
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


class Terrain:
    def __init__(self, elevation: Elevation, explored: bool = False, mist: bool = False):
        """
        Height of terrain determines the terrain Enum value, name, mini-map color, and icon
        This class will also track if the tile has been seen, contains fog, or contains a decoration
        :param elevation: int elevation height
        :param explored: boolean if tile has been in player's fov
        """
        self.elevation = elevation
        self.explored = explored
        # self.decoration = decoration
        self.mist = mist
