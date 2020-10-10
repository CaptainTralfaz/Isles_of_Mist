from __future__ import annotations

from typing import Dict

from constants.enums import Elevation


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
    
    def to_json(self) -> Dict:
        return {
            'elevation': self.elevation.value,
            'explored': self.explored,
            'decoration': self.decoration,
            'mist': self.mist
        }
    
    @staticmethod
    def from_json(json_data: Dict) -> Terrain:
        elevation = json_data.get('elevation')
        explored = json_data.get('explored')
        decoration = json_data.get('decoration')
        mist = json_data.get('mist')
        return Terrain(elevation=Elevation(elevation), explored=explored, decoration=decoration, mist=mist)
