from __future__ import annotations

from typing import TYPE_CHECKING

from action.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor


class RepairSailsAction(Action):
    def __init__(self, entity: Actor):
        """
        repairs the player's sail by 1 (takes 1 hour)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.sails.hp < self.entity.sails.max_hp:
            self.entity.sails.repair(1)
            self.engine.time.roll_hrs(1)
            self.engine.message_log.add_message(f"Repaired 1 Sail (an hour passes)")
            return True
        raise Impossible(f"Sails are already repaired")
