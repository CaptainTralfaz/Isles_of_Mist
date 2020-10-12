from __future__ import annotations

from typing import Optional, Dict, TYPE_CHECKING

from actions.base.base import Action
from constants.enums import GameStates

if TYPE_CHECKING:
    from entity import Entity


class ExitPortAction(Action):
    def __init__(self, entity: Entity):
        """
        This action exits the config menus by setting game state to action (or dead),
            setting all three "selected" fields to be 0 (in case the current selection is destroyed)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> Optional[Dict, bool]:
        if not self.entity.is_alive:
            self.engine.game_state = GameStates.PLAYER_DEAD
            return False
        else:
            self.engine.game_state = GameStates.ACTION
            self.entity.cargo.selected = "arrows"
            self.entity.crew.selected = 0
            self.entity.broadsides.selected = 0
            merchant = self.entity.game_map.port.merchant.manifest
            acted = False
            if sum(self.entity.cargo.sell_list.values()) > 0:  # if there's actually stuff to sell
                # remove the items from player inventory, add to merchant inventory
                for key in self.entity.cargo.sell_list:
                    if self.entity.cargo.sell_list[key] > 0:
                        self.entity.cargo.manifest[key] -= self.entity.cargo.sell_list[key]
                        if not (key in self.engine.game_map.port.merchant.manifest.keys()):
                            self.engine.game_map.port.merchant.manifest[key] = 0
                        self.engine.game_map.port.merchant.manifest[key] += self.entity.cargo.sell_list[key]
                        if key not in merchant.keys():
                            merchant[key] = 0
                        merchant[key] = self.entity.cargo.sell_list[key]
                acted = True
                self.entity.cargo.sell_list = {}
            if sum(self.entity.cargo.buy_list.values()) > 0:  # if there's actually stuff to buy
                # remove the items from merchant inventory, add to player inventory
                for key in self.entity.cargo.buy_list:
                    if self.entity.cargo.buy_list[key] > 0:
                        if key not in self.entity.cargo.manifest.keys():
                            self.entity.cargo.manifest[key] = 0
                        self.entity.cargo.manifest[key] += self.entity.cargo.buy_list[key]
                        merchant[key] -= self.entity.cargo.buy_list[key]
                acted = True
                self.entity.cargo.buy_list = {}
            return acted
