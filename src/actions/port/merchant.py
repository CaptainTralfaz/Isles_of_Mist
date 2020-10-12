from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.port.change_select import ChangeSelectionAction
from constants.enums import MenuKeys
from constants.stats import item_stats

if TYPE_CHECKING:
    from entity import Entity


class MerchantAction(Action):
    def __init__(self, entity: Entity, event: MenuKeys):
        """
        action for buying and selling while the player is in port
        :param entity: acting Entity
        """
        self.entity = entity
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        selected = self.entity.cargo.selected
        
        if self.event == MenuKeys.UP:
            return ChangeSelectionAction(self.entity, self.event).perform()
        elif self.event == MenuKeys.DOWN:
            return ChangeSelectionAction(self.entity, self.event).perform()
        elif self.event == MenuKeys.LEFT:
            # reduce buy list first if able
            if selected in self.entity.cargo.buy_list.keys() and self.entity.cargo.buy_list[selected] > 0:
                self.entity.cargo.buy_list[selected] -= 1
                self.engine.game_map.port.merchant.temp_coins -= item_stats[selected]['cost']
                return False
            # make sure item to sell is in inventory and more than 1
            if selected not in self.entity.cargo.manifest.keys() or self.entity.cargo.manifest[selected] < 1:
                return False
            if selected not in self.entity.cargo.sell_list.keys():
                self.entity.cargo.sell_list[selected] = 1
                self.engine.game_map.port.merchant.temp_coins -= item_stats[selected]['cost']
                return False
            if self.entity.cargo.sell_list[selected] + 1 > self.entity.cargo.manifest[selected]:
                return False
            self.entity.cargo.sell_list[selected] += 1
            self.engine.game_map.port.merchant.temp_coins -= item_stats[selected]['cost']
            return False
        
        elif self.event == MenuKeys.RIGHT:
            # reduce sell list first
            if selected in self.entity.cargo.sell_list.keys() and self.entity.cargo.sell_list[selected] > 0:
                self.entity.cargo.sell_list[selected] -= 1
                self.engine.game_map.port.merchant.temp_coins += item_stats[selected]['cost']
                return False
            if selected not in self.engine.game_map.port.merchant.manifest.keys() \
                    or self.engine.game_map.port.merchant.manifest[selected] < 1:
                return False
            if selected not in self.entity.cargo.buy_list.keys():
                self.entity.cargo.buy_list[selected] = 1
                self.engine.game_map.port.merchant.temp_coins += item_stats[selected]['cost']
                return False
            if self.entity.cargo.buy_list[selected] + 1 > self.engine.game_map.port.merchant.manifest[selected]:
                return False
            self.entity.cargo.buy_list[selected] += 1
            self.engine.game_map.port.merchant.temp_coins += item_stats[selected]['cost']
            return False
        return False
