from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action

if TYPE_CHECKING:
    from entity import Entity


class MerchantAction(Action):
    def __init__(self, entity: Entity):
        """
        action for buying and selling while the player is in port
        :param entity: acting Entity
        """
        self.entity = entity
        self.manifest = {
            'arrows': 200,
            'bolts': 20,
        }
        super().__init__(entity)
    
    def perform(self) -> bool:
        return True
