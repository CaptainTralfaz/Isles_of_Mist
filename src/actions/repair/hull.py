from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor


class RepairHullAction(Action):
    def __init__(self, entity: Actor):
        """
        Repairs the player's hull by 1 point (takes 2 hours)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.fighter.hp < self.entity.fighter.max_hp:
            self.entity.fighter.repair(1)
            self.engine.time.roll_hrs(2)
            self.engine.message_log.add_message(f"Repaired 1 Hull Point (2 hours pass)")
            return True
        raise Impossible(f"Hull is already repaired")
