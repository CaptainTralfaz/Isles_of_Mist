from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from components.crew import Crewman


class Engineer(Action):
    def __init__(self, entity: Entity, crewman: Crewman):
        """
        this action directs the crewman to attempt repairs ballista
        :param entity: acting Entity
        :param crewman: Crewman attempting the action
        """
        self.crewman = crewman
        super().__init__(entity)
    
    def perform(self) -> bool:
        components = ["wood", "leather"]
        if self.crewman.cooldown > 0:
            raise Impossible(f"{self.crewman.name} is still on cooldown")
        damaged_weapons = self.entity.broadsides.get_damaged_weapons()
        repair_list = [weapon for weapon in damaged_weapons if "ballista" in weapon.name.lower()]
        if len(repair_list) < 1:
            raise Impossible(f"There are no damaged Ballista to repair")
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
        self.engine.message_log.add_message(f"{self.crewman.name} repaired {to_repair.name.capitalize()} for 1 point")
        self.engine.message_log.add_message(f"Used 1 {used}")
        return True
