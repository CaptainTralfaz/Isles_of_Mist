from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from constants.enums import GameStates
from utilities import remove_zero_quantities

if TYPE_CHECKING:
    from entity import Entity


class ExitPortAction(Action):
    def __init__(self, entity: Entity, confirm: bool = False):
        """
        This action exits the config menus by setting game state to action (or dead),
            setting all three "selected" fields to be 0 (in case the current selection is destroyed)
        :param entity: acting Entity
        """
        self.confirm = confirm
        super().__init__(entity)
    
    def perform(self) -> bool:
        self.engine.game_state = GameStates.ACTION
        
        self.entity.crew.selected = 0
        self.entity.crew.hire_list = []
        self.entity.crew.release_list = []
        self.entity.game_map.port.tavern.temp_coins = 0
        
        self.entity.broadsides.selected = 0
        self.entity.broadsides.buy_list = []
        self.entity.broadsides.sell_list = []
        self.entity.game_map.port.smithy.temp_coins = 0
        
        self.entity.cargo.selected = "arrows"
        self.entity.cargo.buy_list = {}
        self.entity.cargo.sell_list = {}
        self.entity.game_map.port.merchant.temp_coins = 0
        self.entity.cargo.manifest = remove_zero_quantities(
            self.entity.cargo.manifest)
        self.entity.game_map.port.merchant.manifest = remove_zero_quantities(
            self.entity.game_map.port.merchant.manifest)
        
        return self.confirm
