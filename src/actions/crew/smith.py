from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from components.crew import Crewman


class Smith(Action):
    def __init__(self, entity: Entity, crewman: Crewman):
        """
        this action directs the crewman to attempt repairs ballista
        :param crewman: Crewman attempting the action
        :param entity: acting Entity
        """
        self.crewman = crewman
        super().__init__(entity)
    
    def perform(self) -> bool:
        components = ["iron", "leather"]
        if self.crewman.cooldown > 0:
            raise Impossible(f"{self.crewman.name} is still on cooldown")
        damaged_weapons = self.entity.broadsides.get_damaged_weapons()
        repair_list = [weapon for weapon in damaged_weapons if ("cannon" in weapon.name.lower()
                                                                or "gun" in weapon.name.lower())]
        if len(repair_list) < 1:
            raise Impossible(f"There are no damaged Cannons to repair")
        else:
            to_repair = choice(repair_list)
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
        to_repair.hp += 1
        self.engine.message_log.add_message(f"{self.crewman.name} repaired {to_repair.name} for 1 point")
        self.engine.message_log.add_message(f"Used 1 {used}")
        return True
