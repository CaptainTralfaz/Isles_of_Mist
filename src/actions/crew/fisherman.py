from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from components.crew import Crewman


class Fisherman(Action):
    def __init__(self, entity: Entity, crewman: Crewman):
        """
        this action directs the crewman to attempts to reduce cooldowns
        :param entity: acting Entity
        :param crewman: Crewman attempting the action
        """
        self.crewman = crewman
        super().__init__(entity)
    
    def perform(self) -> bool:
        components = ["meat"]
        if self.crewman.cooldown > 0:
            raise Impossible(f"{self.crewman.name} is still on cooldown")
        for item in components:
            if not (item in self.entity.cargo.manifest.keys() and self.entity.cargo.manifest[item] > 0):
                raise Impossible(f"Cannot fish without {item}")
        self.crewman.cooldown = self.crewman.cooldown_max
        if len(components) > 1:
            used = f"each of {components[0]}"
            for item in components[1:]:
                used = used + f", {item}"
        else:
            used = components[0]
        for item in components:
            self.entity.cargo.manifest[item] -= 1
        fish = randint(0, 3)
        if "fish" in self.entity.cargo.manifest.keys():
            self.entity.cargo.manifest['fish'] += fish
        else:
            self.entity.cargo.manifest['fish'] = fish
        self.engine.message_log.add_message(f"{self.crewman.name} catches {fish} fish")
        self.engine.message_log.add_message(f"Used 1 {used}")
        return True
