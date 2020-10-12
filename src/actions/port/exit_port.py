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
        self.engine.game_state = GameStates.ACTION
        self.entity.crew.selected = 0
        self.entity.broadsides.selected = 0
        self.entity.cargo.selected = "arrows"
        self.entity.cargo.buy_list = {}
        self.entity.cargo.sell_list = {}
        self.entity.game_map.port.merchant.temp_coins = 0
        self.entity.game_map.port.smithy.temp_coins = 0
        return False
