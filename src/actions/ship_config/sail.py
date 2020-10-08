from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor


class SailAction(Action):
    def __init__(self, entity: Actor):
        """
        Toggles the sail
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.sails.hp > 0:
            self.entity.sails.adjust()
            return True
        else:
            raise Impossible("Sails are too damaged to raise")
