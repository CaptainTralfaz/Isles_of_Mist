from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import PortVisit, GameStates
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity


class PortAction(Action):
    def __init__(self, entity: Entity, event: PortVisit):
        """
        this action directs which action should be used while the player is in port
        :param entity: acting Entity
        :param event:
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        # if self.event == PortVisit.SHIPYARD:  # Ship Upgrades
        #     raise Impossible(f"{self.event} action yet implemented")
        if self.event == PortVisit.MERCHANT:  # Buy / sell Cargo
            self.engine.game_state = GameStates.MERCHANT
            return False
        if self.event == PortVisit.TAVERN:  # Hire Crewmen
            self.engine.game_state = GameStates.TAVERN
            return False
        if self.event == PortVisit.SMITHY:  # Buy / Sell Weapons
            self.engine.game_state = GameStates.SMITHY
            return False
        
        raise Impossible(f"{self.event} action yet implemented")
