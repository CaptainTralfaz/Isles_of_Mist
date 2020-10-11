from __future__ import annotations

from typing import Optional, Dict, TYPE_CHECKING

from actions.base.base import Action
from constants.enums import GameStates

if TYPE_CHECKING:
    from entity import Entity


class ExitConfigAction(Action):
    def __init__(self, entity: Entity):
        """
        This action exits the config menus by setting game state to action (or dead),
            setting all three "selected" fields to be 0 (in case the current selection is destroyed)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> Optional[Dict, bool]:
        if self.entity.is_alive:
            self.engine.game_state = GameStates.ACTION
            self.entity.cargo.selected = "arrows"
            self.entity.crew.selected = 0
            self.entity.broadsides.selected = 0
            if sum(self.entity.cargo.sell_list.values()) > 0:  # if there's actually stuff to drop
                # remove the items from inventory
                for key in self.entity.cargo.sell_list:
                    self.entity.cargo.manifest[key] -= self.entity.cargo.sell_list[key]
                # and create a dict to pass back for creation
                entity_dict = {
                    'x': self.entity.x,
                    'y': self.entity.y,
                    'elevations': 'ocean',
                    'name': 'Chest',
                    'icon': 'chest',
                    'cargo': self.entity.cargo.sell_list
                }
                self.entity.cargo.sell_list = {}
                return entity_dict
            return False
        else:
            self.engine.game_state = GameStates.PLAYER_DEAD
        return False
