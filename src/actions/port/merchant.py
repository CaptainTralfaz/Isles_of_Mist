from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.port.change_select import ChangeSelectionAction
from constants.enums import MenuKeys

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
        manifest = self.entity.cargo.manifest
        selected = self.entity.cargo.selected
        sell_list = self.entity.cargo.sell_list
        buy_list = self.entity.cargo.buy_list
        merchant = self.engine.game_map.port.merchant.manifest
        
        if self.event == MenuKeys.UP:
            return ChangeSelectionAction(self.entity, self.event, self.engine.game_state).perform()
        elif self.event == MenuKeys.DOWN:
            return ChangeSelectionAction(self.entity, self.event, self.engine.game_state).perform()
        elif self.event == MenuKeys.LEFT:
            # reduce buy list first if able
            if selected in buy_list.keys() and buy_list[selected] > 0:
                buy_list[selected] -= 1
                return False
            # make sure item to sell is in inventory and more than 1
            if selected not in manifest.keys() or manifest[selected] < 1:
                return False
            if selected not in sell_list.keys():
                sell_list[selected] = 1
                return False
            if sell_list[selected] + 1 > manifest[selected]:
                return False
            sell_list[selected] += 1
        elif self.event == MenuKeys.RIGHT:
            # reduce sell list first
            if selected in sell_list.keys() and sell_list[selected] > 0:
                sell_list[selected] -= 1
                return False
            if selected not in merchant.keys() or merchant[selected] < 1:
                return False
            if selected not in buy_list.keys():
                buy_list[selected] = 1
                return False
            if buy_list[selected] + 1 > merchant[selected]:
                return False
            buy_list[selected] += 1
        return False
