from components.base import BaseComponent
from entity import Actor


class View(BaseComponent):
    parent: Actor
    
    def __init__(self, view: int) -> None:
        """
        Component detailing an entity's view
        :param view: int distance in hexes an entity can "see"
        """
        self.view = view
        self.fov = {}
    
    def set_fov(self) -> None:
        """
        # :param game_map: the current map being played on
        # :param game_time: current game Time
        # :param game_weather: current map Weather conditions
        :return: Nothing - modify current map
        """
        # get list of visible tiles
        # port = None
        # visible_tiles = get_fov(self, game_map=game_map, game_time=game_time, game_weather=game_weather)
        
        visible_tiles = self.parent.game_map.get_fov(self.view, self.parent.x, self.parent.y)
        
        # if self.owner.name == 'player':
        #     for (x, y) in visible_tiles:
        #         if (0 <= x < game_map.width) and (0 <= y < game_map.height) and not game_map.terrain[x][y].seen:
        #             game_map.terrain[x][y].seen = True
        # else:  # not the player, remove port from fov
        #     # print(visible_tiles, len(visible_tiles))
        #     for x, y in visible_tiles:
        #         if game_map.terrain[x][y].decoration and game_map.terrain[x][y].decoration.name == 'Port':
        #             port = (x, y)

        for (x, y) in visible_tiles:
            if self.parent.game_map.in_bounds(x, y) and not self.parent.game_map.terrain[x][y].explored:
                self.parent.game_map.terrain[x][y].explored = True
        # if port:
        #     visible_tiles.remove(port)
        # # replace old visible list
        # self.fov = visible_tiles
        # # print(self.owner.name, self.fov)
