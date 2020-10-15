from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import MenuKeys
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class AssignCargoAction(Action):
    def __init__(self, entity: Entity, event: Enum):
        """
        "assigns" selected crewman to a directional button
        :param entity: acting Entity
        :param event: direction key assigning crew to
        """
        super().__init__(entity)
        self.event = event
    
    def perform(self) -> bool:
        cargo = self.entity.cargo
        item = self.entity.cargo.selected
        
        if not self.entity.is_alive:
            raise Impossible("Can't move cargo when dead")

        # move marked inventory to drop list
        if self.event == MenuKeys.LEFT:
            if item in cargo.manifest.keys() and cargo.manifest[item] > 0:
                if item in cargo.sell_list.keys():
                    cargo.sell_list[item] += 1
                else:
                    cargo.sell_list[item] = 1
                if cargo.sell_list[item] > cargo.manifest[item]:
                    cargo.sell_list[item] = cargo.manifest[item]
        # remove marked inventory from drop list
        elif self.event == MenuKeys.RIGHT:
            if item in cargo.sell_list.keys() and cargo.sell_list[item] > 0:
                if item in cargo.sell_list.keys():
                    cargo.sell_list[item] -= 1
        
        return False
