from components.base import BaseComponent
from entity import Actor
from tile import Elevation


class View(BaseComponent):
    parent: Actor
    
    def __init__(self, distance: int) -> None:
        """
        Component detailing an entity's view
        :param distance: int distance in hexes an entity can "see"
        """
        self.distance = distance
        self.fov = {}
    
    def set_fov(self) -> None:
        """
        :return: Nothing - modify current map
        """
        if self.parent.flying:
            elevation = Elevation.JUNGLE
        else:
            elevation = Elevation.SHALLOWS
        visible_tiles = self.parent.game_map.get_fov(self.distance,
                                                     self.parent.x,
                                                     self.parent.y,
                                                     elevation=elevation)
        for (x, y) in visible_tiles:
            if self.parent.name == "Player" \
                    and self.parent.game_map.in_bounds(x, y) \
                    and not self.parent.game_map.terrain[x][y].explored:
                self.parent.game_map.terrain[x][y].explored = True
        self.fov = visible_tiles
