from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible
from constants.enums import GameStates

if TYPE_CHECKING:
    from entity import Actor
    from enum import Enum


class AssignCrewAction(Action):
    def __init__(self, entity: Actor, event: Enum):
        """
        "assigns" selected crewman to a directional button
        :param entity: acting Entity
        :param event: direction key assigning crew to
        """
        super().__init__(entity)
        self.event = event
    
    def perform(self) -> bool:
        if not self.entity.is_alive:
            raise Impossible("Can't assign crew when dead")
        if self.entity.crew.assignments[self.event] == self.entity.crew.roster[self.entity.crew.selected]:
            self.entity.crew.assignments[self.event] = None
            self.engine.message_log.add_message(f"assigning nobody to '{self.event}' key")
            return False
        else:
            self.entity.crew.assignments[self.event] = self.entity.crew.roster[self.entity.crew.selected]
            self.engine.message_log.add_message(f"assigning {self.entity.crew.roster[self.entity.crew.selected].name}"
                                                f" to '{self.event}' key")
            self.engine.game_state = GameStates.ACTION
            return True
