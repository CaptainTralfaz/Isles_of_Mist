from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.port.merchant import MerchantAction
from actions.ship_config.drop_cargo import DropCargoAction
from constants.enums import GameStates, MenuKeys

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class SelectedAction(Action):
    def __init__(self, entity: Entity, event: MenuKeys, state: GameStates):
        """
        this action directs which action should be used when the highlighted item in a list is
            selected for another action
        :param entity: acting Entity
        :param event: the event taking place
        :param state: GameState
        """
        self.event = event
        self.state = state
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.state == GameStates.MERCHANT:
            return MerchantAction(self.entity, self.event).perform()
        if self.state == GameStates.SMITHY:
            return TradeAction(self.entity, self.event, self.state).perform()
        if self.state == GameStates.UPGRADES:
            return UpgradeAction(self.entity, self.event).perform()
        return False
