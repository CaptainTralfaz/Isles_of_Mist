from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import GameStates, MenuKeys
from constants.keys import MENU_KEYS
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class DropCargoAction(Action):
    def __init__(self, entity: Entity, event: Enum):
        """
        "assigns" selected crewman to a directional button
        :param entity: acting Entity
        :param event: direction key assigning crew to
        """
        super().__init__(entity)
        self.count = 0
        self.event = event
    
    def perform(self) -> bool:
        if not self.entity.is_alive:
            raise Impossible("Can't drop cargo when dead")
        
        item_list = list(self.entity.cargo.manifest.keys())
        item = item_list[self.entity.cargo.selected]
        
        if self.event == MenuKeys.LEFT:
            self.count -= 1
        elif self.event == MenuKeys.RIGHT:
            self.count += 1
        
        return False
