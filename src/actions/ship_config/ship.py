from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.ship_config.configure import ConfigureAction
from actions.ship_config.sail import SailAction
from constants.enums import ShipConfig

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class ShipAction(Action):
    def __init__(self, entity: Entity, event: Enum):
        """
        this action directs which action should be used during a ship configure action
        :param entity: acting Entity
        :param event: toggle sails or configure
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event == ShipConfig.SAILS:
            return SailAction(self.entity).perform()
        else:
            return ConfigureAction(self.entity, self.event).perform()
