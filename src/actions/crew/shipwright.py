from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from components.crew import Crewman


class Shipwright(Action):
    def __init__(self, entity: Entity, crewman: Crewman):
        """
        this action directs the crewman to attempt repairs on the ship
        :param entity: acting Entity
        """
        self.crewman = crewman
        super().__init__(entity)
    
    def perform(self) -> bool:
        components = ["wood", "tar"]
        if self.crewman.cooldown > 0:
            raise Impossible(f"{self.crewman.name} is still on cooldown")
        if self.entity.fighter.hp >= self.entity.fighter.max_hp:
            raise Impossible(f"{self.entity.fighter.name.capitalize()} is not in need of repairs")
        for item in components:
            if not (item in self.entity.cargo.manifest.keys() and self.entity.cargo.manifest[item] > 0):
                raise Impossible(f"Cannot repair without {item}")
        self.crewman.cooldown = self.crewman.cooldown_max
        if len(components) > 1:
            used = f"each of {components[0]}"
            for item in components[1:]:
                used = used + f", {item}"
        else:
            used = components[0]
        for item in components:
            self.entity.cargo.manifest[item] -= 1
        self.entity.fighter.hp += 1
        self.engine.message_log.add_message(f"{self.crewman.name} repaired {self.entity.fighter.name} for 1 point")
        self.engine.message_log.add_message(f"Used 1 {used}")
        return True
