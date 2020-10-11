from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import GameStates, MenuKeys
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class ChangeSelectionAction(Action):
    def __init__(self, entity: Entity, event: Enum, state: GameStates):
        """
        this action moves the selector up or down in the config menus
        :param entity: acting Entity
        :param event: the key pressed
        :param state: GameState
        """
        self.event = event
        self.state = state
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.state == GameStates.MERCHANT:
            component = self.entity.game_map.port.merchant
            length = len(self.entity.game_map.port.merchant.manifest.keys()) - 1
        elif self.state == GameStates.SMITHY:
            component = self.entity.game_map.port.smithy
            length = len(self.entity.game_map.port.smithy.manifest.keys()) - 1
        else:
            raise Impossible("Bad State")
        
        if self.event == MenuKeys.UP:
            component.selected -= 1
            if component.selected < 0:
                component.selected = length
        if self.event == MenuKeys.DOWN:
            component.selected += 1
            if component.selected > length:
                component.selected = 0
        return False
