from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity


class RepairHullAction(Action):
    def __init__(self, entity: Entity):
        """
        Repairs the player's hull by 1 point (takes 2 hours)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.fighter.hp >= self.entity.fighter.max_hp:
            raise Impossible(f"Hull is already fully repaired")
        if self.entity.cargo.coins < 20:
            raise Impossible("Not enough coins")
        self.entity.cargo.coins -= 20
        self.entity.fighter.repair(1)
        self.engine.time.roll_hrs(2)
        self.engine.message_log.add_message(f"Repaired 1 Hull Point for 20 Coins (2 hours pass)")
        return True
