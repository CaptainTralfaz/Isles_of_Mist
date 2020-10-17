from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import GameStates, MenuKeys
from constants.stats import item_stats

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class ChangeSelectionAction(Action):
    def __init__(self, entity: Entity, event: Enum):
        """
        this action moves the selector up or down in the config menus
        :param entity: acting Entity
        :param event: the key pressed
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.engine.game_state == GameStates.MERCHANT:
            manifest_keys = [key for key in self.entity.cargo.manifest.keys()]
            merchant_keys = [key for key in self.entity.game_map.port.merchant.manifest.keys()]
            
            all_keys = sorted(list(set(manifest_keys) | set(merchant_keys)),
                              key=lambda i: item_stats[i]['category'].value)
            
            count = 0
            for key in all_keys:
                if key == self.entity.cargo.selected:
                    break
                count += 1
            
            if self.event == MenuKeys.UP:
                count -= 1
                if count < 0:
                    count = len(all_keys) - 1
                self.entity.cargo.selected = all_keys[count]
            if self.event == MenuKeys.DOWN:
                count += 1
                if count >= len(all_keys):
                    count = 0
                self.entity.cargo.selected = all_keys[count]
            return False
        
        elif self.engine.game_state == GameStates.SMITHY:
            length = len(self.entity.broadsides.storage) + len(self.entity.game_map.port.smithy.manifest) - 1
            if self.event == MenuKeys.UP:
                self.entity.broadsides.selected -= 1
                if self.entity.broadsides.selected < 0:
                    self.entity.broadsides.selected = length
            if self.event == MenuKeys.DOWN:
                self.entity.broadsides.selected += 1
                if self.entity.broadsides.selected > length:
                    self.entity.broadsides.selected = 0
        
        elif self.engine.game_state == GameStates.TAVERN:
            length = len(self.entity.crew.roster) + len(self.entity.game_map.port.tavern.roster) - 1
            if self.event == MenuKeys.UP:
                self.entity.crew.selected -= 1
                if self.entity.crew.selected < 0:
                    self.entity.crew.selected = length
            if self.event == MenuKeys.DOWN:
                self.entity.crew.selected += 1
                if self.entity.crew.selected > length:
                    self.entity.crew.selected = 0
        
        return False
