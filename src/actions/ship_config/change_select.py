from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import GameStates, MenuKeys
from constants.stats import item_stats
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
        if self.state == GameStates.CARGO_CONFIG:
            manifest_keys = sorted([key for key in self.entity.cargo.manifest.keys()],
                                   key=lambda i: item_stats[i]['category'].value)
            count = 0
            for key in manifest_keys:
                if key == self.entity.cargo.selected:
                    break
                count += 1
            
            if self.event == MenuKeys.UP:
                count -= 1
                if count < 0:
                    count = len(manifest_keys) - 1
                self.entity.cargo.selected = manifest_keys[count]
            if self.event == MenuKeys.DOWN:
                count += 1
                if count >= len(manifest_keys):
                    count = 0
                self.entity.cargo.selected = manifest_keys[count]
            return False
        
        elif self.state == GameStates.WEAPON_CONFIG:
            component = self.entity.broadsides
            length = len(self.entity.broadsides.all_weapons) - 1
        elif self.state == GameStates.CREW_CONFIG:
            component = self.entity.crew
            length = len(self.entity.crew.roster) - 1
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
