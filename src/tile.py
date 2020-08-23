from enum import auto, Enum


class Elevation(Enum):
    """
    Enum to track elevation
    """
    DEEPS = auto()
    WATER = auto()
    SHALLOWS = auto()
    DUNES = auto()
    GRASSLAND = auto()
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
    def __init__(self, elevation: int, seen: bool = False):
        """
        Height of terrain determines the terrain Enum value, name, mini-map color, and icon
        This class will also track if the tile has been seen, contains fog, or contains a decoration
        :param elevation: int elevation height
        :param seen: boolean if tile has been in player's fov
        """
        self.elevation = Elevation(elevation)
        self.seen = seen
        self.movable = False if elevation > 2 else True
        # self.decoration = decoration
        # self.fog = fog
        
        if self.elevation == Elevation.DEEPS:
            self.name = 'Deep Sea'
            self.icon = 'deep_sea'
            # self.color = 'light_blue'
        elif self.elevation == Elevation.WATER:
            self.name = 'Sea'
            self.icon = 'sea'
            # self.color = 'blue'
        elif self.elevation == Elevation.SHALLOWS:
            self.name = 'Shallows'
            self.icon = 'shallows'
            # self.color = 'aqua'
        elif self.elevation == Elevation.DUNES:
            self.name = 'Dunes'
            self.icon = 'dunes'
            # self.color = 'cantaloupe'
        elif self.elevation == Elevation.GRASSLAND:
            self.name = 'Grassland'
            self.icon = 'grassland'
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
