from __future__ import annotations

from typing import TYPE_CHECKING

from action.base import Action
from custom_exceptions import Impossible

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
        if self.event == "merchant":
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == "barracks":
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == "shipyard":
            raise Impossible(f"{self.event} action yet implemented")
        if self.event == "tavern":
            raise Impossible(f"{self.event} action yet implemented")
        return True
