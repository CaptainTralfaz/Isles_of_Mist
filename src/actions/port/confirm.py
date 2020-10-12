from __future__ import annotations

from typing import Optional, Dict, TYPE_CHECKING

from actions.base.base import Action
from actions.port.exit_port import ExitPortAction
from constants.enums import GameStates, MenuKeys

if TYPE_CHECKING:
    from entity import Entity


class ConfirmAction(Action):
    def __init__(self, entity: Entity, event: MenuKeys):
        """
        This action exits the config menus by setting game state to action (or dead),
            setting all three "selected" fields to be 0 (in case the current selection is destroyed)
        :param entity: acting Entity
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> Optional[Dict, bool]:
        if not self.entity.is_alive:
            self.engine.game_state = GameStates.PLAYER_DEAD
            return False
        elif self.event == MenuKeys.LEFT:
            return ExitPortAction(self.entity).perform()
        else:
            # make sure there is enough money
            if self.entity.cargo.coins - self.entity.game_map.port.merchant.temp_coins < 0:
                self.engine.message_log.add_message("You don't have enough coins...")
                self.entity.cargo.sell_list = {}
                self.entity.cargo.buy_list = {}
                self.entity.game_map.port.merchant.temp_coins = 0
                return False
            
            if self.entity.game_map.port.merchant.coins + self.entity.game_map.port.merchant.temp_coins < 0:
                self.engine.message_log.add_message("Merchant doesn't have enough coins...")
                self.entity.cargo.sell_list = {}
                self.entity.cargo.buy_list = {}
                self.entity.game_map.port.merchant.temp_coins = 0
                return False
            
            self.engine.game_state = GameStates.ACTION
            self.entity.cargo.selected = "arrows"
            self.entity.crew.selected = 0
            self.entity.broadsides.selected = 0
            
            if sum(self.entity.cargo.sell_list.values()) > 0:  # if there's actually stuff to sell
                # remove the items from player inventory, add to merchant inventory
                for key in self.entity.cargo.sell_list:
                    if self.entity.cargo.sell_list[key] > 0:
                        self.entity.cargo.manifest[key] -= self.entity.cargo.sell_list[key]
                        if not (key in self.engine.game_map.port.merchant.manifest.keys()):
                            self.engine.game_map.port.merchant.manifest[key] = 0
                        self.engine.game_map.port.merchant.manifest[key] += self.entity.cargo.sell_list[key]
                        if key not in self.entity.game_map.port.merchant.manifest.keys():
                            self.entity.game_map.port.merchant.manifest[key] = 0
                        self.entity.game_map.port.merchant.manifest[key] = self.entity.cargo.sell_list[key]
                self.entity.cargo.sell_list = {}
            
            if sum(self.entity.cargo.buy_list.values()) > 0:  # if there's actually stuff to buy
                # remove the items from merchant inventory, add to player inventory
                for key in self.entity.cargo.buy_list:
                    if self.entity.cargo.buy_list[key] > 0:
                        if key not in self.entity.cargo.manifest.keys():
                            self.entity.cargo.manifest[key] = 0
                        self.entity.cargo.manifest[key] += self.entity.cargo.buy_list[key]
                        self.entity.game_map.port.merchant.manifest[key] -= self.entity.cargo.buy_list[key]
                self.entity.cargo.buy_list = {}
            
            self.entity.cargo.coins -= self.entity.game_map.port.merchant.temp_coins
            self.entity.game_map.port.merchant.coins += self.entity.game_map.port.merchant.temp_coins
            self.entity.game_map.port.merchant.temp_coins = 0
            self.engine.message_log.add_message("Transaction completed")
        
        return True
