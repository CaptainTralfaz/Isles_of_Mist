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
    def __init__(self, elevation: Elevation, explored: bool = False):
        """
        Height of terrain determines the terrain Enum value, name, mini-map color, and icon
        This class will also track if the tile has been seen, contains fog, or contains a decoration
        :param elevation: int elevation height
        :param explored: boolean if tile has been in player's fov
        """
        self.elevation = elevation
        self.explored = explored
        self.movable = True if elevation <= Elevation.SHALLOWS else True
        # self.decoration = decoration
        # self.fog = fog
        
        if self.elevation == Elevation.OCEAN:
            self.name = 'Ocean'
            self.icon = 'ocean'
            # self.color = 'light_blue'
        elif self.elevation == Elevation.WATER:
            self.name = 'Water'
            self.icon = 'water'
            # self.color = 'blue'
        elif self.elevation == Elevation.SHALLOWS:
            self.name = 'Shallows'
            self.icon = 'shallows'
            # self.color = 'aqua'
        elif self.elevation == Elevation.BEACH:
            self.name = 'Beach'
            self.icon = 'beach'
            # self.color = 'cantaloupe'
        elif self.elevation == Elevation.GRASS:
            self.name = 'Grass'
            self.icon = 'grass'
            # self.color = 'light_green'
        elif self.elevation == Elevation.JUNGLE:
            self.name = 'Jungle'
            self.icon = 'jungle'
            # self.color = 'medium_green'
        elif self.elevation == Elevation.MOUNTAIN:
            self.name = 'Mountain'
            self.icon = 'mountain'
            # self.color = 'text'
        elif self.elevation == Elevation.VOLCANO:
            self.name = 'Volcano'
            self.icon = 'volcano'
            # self.color = 'light_red'
