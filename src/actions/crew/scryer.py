from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import Elevation
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from components.crew import Crewman


class Scryer(Action):
    def __init__(self, entity: Entity, crewman: Crewman):
        """
        this action directs the crewman to attempts to make the weather worse
        :param entity: acting Entity
        :param crewman: Crewman attempting the action
        """
        self.crewman = crewman
        super().__init__(entity)
    
    def perform(self) -> bool:
        components = ["pearl"]
        if self.crewman.cooldown > 0:
            raise Impossible(f"{self.crewman.name} is still on cooldown")
        for item in components:
            if not (item in self.entity.cargo.manifest.keys() and self.entity.cargo.manifest[item] > 0):
                raise Impossible(f"Cannot view without {item}")
        self.crewman.cooldown = self.crewman.cooldown_max
        if len(components) > 1:
            used = f"each of {components[0]}"
            for item in components[1:]:
                used = used + f", {item}"
        else:
            used = components[0]
        for item in components:
            self.entity.cargo.manifest[item] -= 1
        
        distance = self.entity.view.distance + 2
        visible_tiles = self.entity.game_map.get_fov(distance,
                                                     self.entity.x,
                                                     self.entity.y,
                                                     elevation=Elevation.ALL,
                                                     mist_view=distance)
        for (x, y) in visible_tiles:
            if self.entity.name == "Player" \
                    and self.entity.game_map.in_bounds(x, y) \
                    and not self.entity.game_map.terrain[x][y].explored:
                self.entity.game_map.terrain[x][y].explored = True
        
        self.engine.message_log.add_message(f"{self.crewman.name} views from on high!", text_color='yellow')
        self.engine.message_log.add_message(f"Used 1 {used}")
        return True
