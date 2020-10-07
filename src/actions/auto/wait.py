from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base import Action

if TYPE_CHECKING:
    from entity import Actor


class WaitAction(Action):
    def __init__(self, entity: Actor):
        """
        skips an Entity's turn
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.sails and self.entity.sails.raised:
            self.engine.message_log.add_message(f"{self.entity.name} coasts...")
        else:
            self.engine.message_log.add_message(f"{self.entity.name} waits...")
        return True
