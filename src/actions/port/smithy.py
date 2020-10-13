from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.port.change_select import ChangeSelectionAction
from constants.enums import MenuKeys
from constants.stats import item_stats

if TYPE_CHECKING:
    from entity import Entity


class SmithyAction(Action):
    def __init__(self, entity: Entity, event: MenuKeys):
        """
        action for buying and selling while the player is in port
        :param entity: acting Entity
        """
        self.entity = entity
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        weapon_list = []
        for weapon in self.entity.broadsides.storage:
            weapon_list.append(weapon)
        for weapon in self.entity.game_map.port.smithy.manifest:
            weapon_list.append(weapon)
        selected = self.entity.broadsides.selected
        
        storage = self.entity.broadsides.storage
        sell_list = self.entity.broadsides.sell_list
        buy_list = self.entity.broadsides.buy_list
        smithy = self.entity.game_map.port.smithy.manifest
        
        if self.event == MenuKeys.UP:
            return ChangeSelectionAction(self.entity, self.event).perform()
        elif self.event == MenuKeys.DOWN:
            return ChangeSelectionAction(self.entity, self.event).perform()
        
        elif self.event == MenuKeys.LEFT:
            if weapon_list[selected] in sell_list:
                sell_list.remove(weapon_list[selected])
                self.entity.game_map.port.smithy.temp_coins += item_stats[weapon_list[selected].name.lower()]['cost']
            elif weapon_list[selected] in smithy:
                buy_list.append(weapon_list[selected])
                self.entity.game_map.port.smithy.temp_coins += item_stats[weapon_list[selected].name.lower()]['cost']
            return False
        
        elif self.event == MenuKeys.RIGHT:
            if weapon_list[selected] in buy_list:
                buy_list.remove(weapon_list[selected])
                self.entity.game_map.port.smithy.temp_coins -= item_stats[weapon_list[selected].name.lower()]['cost']
            elif weapon_list[selected] in storage:
                sell_list.append(weapon_list[selected])
                self.entity.game_map.port.smithy.temp_coins -= item_stats[weapon_list[selected].name.lower()]['cost']
            return False
        
        return False
