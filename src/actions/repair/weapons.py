from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity


class RepairWeaponsAction(Action):
    def __init__(self, entity: Entity):
        """
        repairs the player's weapons by 1 each (takes 1 hour each)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        damaged = self.entity.broadsides.get_damaged_weapons()
        if len(damaged) <= 0:
            raise Impossible(f"Weapons are already fully repaired")
        if self.entity.cargo.coins < 25:
            raise Impossible(f"Not enough coins")
        self.entity.cargo.coins -= 25
        weapon = choice(damaged)
        weapon.repair(1)
        self.engine.time.roll_hrs(1)
        self.engine.message_log.add_message(f"Repaired 1 {weapon.name} damage (one hour passes)")
        return True
