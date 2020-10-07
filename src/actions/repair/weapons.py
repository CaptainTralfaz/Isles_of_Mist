from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor


class RepairWeaponsAction(Action):
    def __init__(self, entity: Actor):
        """
        repairs the player's weapons by 1 each (takes 1 hour each)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        damaged = self.entity.broadsides.get_damaged_weapons()
        hrs = 0
        if damaged:
            for weapon in damaged:
                weapon.repair(1)
                hrs += 1
        if hrs:
            hours = "hours" if hrs > 1 else "hour"
            passes = "pass" if hrs > 1 else "passes"
            self.engine.time.roll_hrs(hrs)
            self.engine.message_log.add_message(f"Repaired {hrs} Weapons damage ({hrs} {hours} {passes})")
            return True
        raise Impossible(f"Weapons are already fully repaired")
