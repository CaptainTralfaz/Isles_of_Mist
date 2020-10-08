from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor


class HireCrewAction(Action):
    def __init__(self, entity: Actor):
        """
        "hires" 1 crew member, takes 1 hour (this will move to port actions in the future)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.crew.count < self.entity.crew.max_count:
            self.entity.crew.hire(1)
            self.engine.time.roll_hrs(1)
            self.engine.message_log.add_message(f"Hired 1 Sailor (an hour passes)")
            return True
        raise Impossible(f"Crew is full!")
