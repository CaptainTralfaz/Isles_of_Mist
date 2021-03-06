from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import Conditions
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from components.crew import Crewman


class StormBringer(Action):
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
                raise Impossible(f"Cannot change weather without {item}")
        if self.entity.game_map.weather.conditions == Conditions.STORMY:
            raise Impossible(f"Weather conditions cannot get worse")
        self.crewman.cooldown = self.crewman.cooldown_max
        if len(components) > 1:
            used = f"each of {components[0]}"
            for item in components[1:]:
                used = used + f", {item}"
        else:
            used = components[0]
        for item in components:
            self.entity.cargo.manifest[item] -= 1
        self.entity.game_map.weather.conditions = Conditions(self.entity.game_map.weather.conditions.value + 1)
        self.entity.game_map.weather.conditions_count = 0
        self.engine.message_log.add_message(f"{self.crewman.name} moves the heavens!", text_color='yellow')
        self.engine.message_log.add_message(f"Used 1 {used}")
        return True
