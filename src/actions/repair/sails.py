from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity


class RepairSailsAction(Action):
    def __init__(self, entity: Entity):
        """
        repairs the player's sail by 1 (takes 1 hour)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.sails.hp >= self.entity.sails.max_hp:
            raise Impossible("Sails are already fully repaired")
        if self.entity.cargo.coins < 15:
            raise Impossible("Not enough coins!")
        self.entity.cargo.coins -= 15
        self.entity.sails.repair(1)
        self.engine.time.roll_hrs(1)
        self.engine.message_log.add_message(f"Repaired 1 Sail (one hour passes)")
        return True
