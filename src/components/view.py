from components.base import BaseComponent
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
        
    def set_fov(self) -> None:
        """
        :return: Nothing - modify current map
        """
        
        # TODO if sailing
        visible_tiles = self.parent.game_map.get_ocean_fov(self.distance, self.parent.x, self.parent.y)
        # print(self.parent.name, visible_tiles)
        # TODO else flying
        # visible_tiles = self.parent.game_map.get_AIR_fov(self.distance, self.parent.x, self.parent.y)

        for (x, y) in visible_tiles:
            if self.parent.name == "Player" \
                    and self.parent.game_map.in_bounds(x, y) \
                    and not self.parent.game_map.terrain[x][y].explored:
                self.parent.game_map.terrain[x][y].explored = True
        self.fov = visible_tiles
