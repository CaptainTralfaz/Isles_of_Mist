from __future__ import annotations

from typing import TYPE_CHECKING

from components.base import BaseComponent
from constants.enums import Elevation

if TYPE_CHECKING:
    from entity import Actor


class View(BaseComponent):
    parent: Actor
    
    def __init__(self, distance: int) -> None:
        """
        Component detailing an entity's view
        :param distance: int distance in hexes an entity can "see"
        """
        self.distance = distance
        self.fov = {}
    
    def to_json(self):
        return {
            'distance': self.distance
        }
    
    def set_fov(self) -> None:
        distance = self.distance + self.engine.time.get_time_of_day_info['view'] + \
                   self.game_map.weather.get_weather_info['view']
        if distance < 1:
            distance = 1
        if self.parent.flying or (self.parent.x, self.parent.y) == self.parent.game_map.port.location:
            elevation = Elevation.JUNGLE
        else:
            elevation = Elevation.SHALLOWS
        visible_tiles = self.parent.game_map.get_fov(distance,
                                                     self.parent.x,
                                                     self.parent.y,
                                                     elevation=elevation)
        if self.parent.name != "Player" and self.parent.game_map.port.location in visible_tiles:
            visible_tiles.remove(self.parent.game_map.port.location)
        for (x, y) in visible_tiles:
            if self.parent.name == "Player" \
                    and self.parent.game_map.in_bounds(x, y) \
                    and not self.parent.game_map.terrain[x][y].explored:
                self.parent.game_map.terrain[x][y].explored = True
        self.fov = visible_tiles
