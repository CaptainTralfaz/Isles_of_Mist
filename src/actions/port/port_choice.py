from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base import Action
from custom_exceptions import Impossible
from constants.enums import GameStates, PortVisit

if TYPE_CHECKING:
    from entity import Actor


class PortAction(Action):
    def __init__(self, entity: Actor, event: str):
        """
        this action directs which action should be used while the player is in port
        :param entity: acting Entity
        :param event:
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event == PortVisit.SHIPYARD:
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == PortVisit.MERCHANT:
            # self.engine.game_state = GameStates.MERCHANT
            # return False
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == PortVisit.TAVERN:
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == PortVisit.SMITHY:
            raise Impossible(f"{self.event} action yet implemented")
        return False
