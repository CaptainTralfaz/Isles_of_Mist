from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.port.merchant import MerchantAction
from actions.port.smithy import SmithyAction
from constants.enums import GameStates, MenuKeys

if TYPE_CHECKING:
    from entity import Entity


class SelectedAction(Action):
    def __init__(self, entity: Entity, event: MenuKeys):
        """
        this action directs which action should be used when the highlighted item in a list is
            selected for another action
        :param entity: acting Entity
        :param event: the event taking place
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.engine.game_state == GameStates.MERCHANT:
            return MerchantAction(self.entity, self.event).perform()
        if self.engine.game_state == GameStates.SMITHY:
            return SmithyAction(self.entity, self.event).perform()
        if self.engine.game_state == GameStates.UPGRADES:
            return UpgradeAction(self.entity, self.event).perform()
        return False
