from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import PortVisit

if TYPE_CHECKING:
    from entity import Entity


class SmithyAction(Action):
    def __init__(self, entity: Entity, event: PortVisit):
        """
        action for buying and selling while the player is in port
        :param entity: acting Entity
        """
        self.entity = entity
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        return False
