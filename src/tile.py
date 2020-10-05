from enums import Elevation


class Terrain:
    def __init__(self, elevation: Elevation, explored: bool = False, decoration: str = None, mist: bool = False):
        """
        Height of terrain determines the terrain Enum value, name, mini-map color, and icon
        This class will also track if the tile has been seen, contains fog, or contains a decoration
        :param elevation: int elevation height
        :param explored: boolean if tile has been in player's fov
        """
        self.elevation = elevation
        self.explored = explored
        self.decoration = decoration
        self.mist = mist
