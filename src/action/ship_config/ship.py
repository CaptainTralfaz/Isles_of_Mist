from __future__ import annotations

from typing import TYPE_CHECKING

from action.base import Action
from action.ship_config.configure import ConfigureAction
from action.ship_config.sail import SailAction

if TYPE_CHECKING:
    from entity import Actor
    from constants.enums import GameStates


class ShipAction(Action):
    def __init__(self, entity: Actor, event: str, status: GameStates):
        """
        this action directs which action should be used during a ship configure action
        :param entity: acting Entity
        :param event: toggle sails or configure
        :param status: Game State
        """
        self.event = event
        self.status = status
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event == "sails":
            return SailAction(self.entity).perform()
        else:
            return ConfigureAction(self.entity, self.event, self.status).perform()
