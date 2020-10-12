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
        :param state: GameState
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
        
        # elif self.state == GameStates.SMITHY:
        #     component = self.entity.game_map.port.smithy
        #     length = len(self.entity.game_map.port.smithy.manifest.keys()) - 1
        # else:
        #     raise Impossible("Bad State")
        #
        # if self.event == MenuKeys.UP:
        #     component.selected -= 1
        #     if component.selected < 0:
        #         component.selected = length
        # if self.event == MenuKeys.DOWN:
        #     component.selected += 1
        #     if component.selected > length:
        #         component.selected = 0
        return False
