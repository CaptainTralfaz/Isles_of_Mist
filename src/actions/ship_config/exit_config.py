from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base import Action
from constants.enums import GameStates

if TYPE_CHECKING:
    from entity import Actor


class ExitConfigAction(Action):
    def __init__(self, entity: Actor):
        """
        This action exits the config menus by setting game state to action (or dead),
            setting all three "selected" fields to be 0 (in case the current selection is destroyed)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.is_alive:
            self.engine.game_state = GameStates.ACTION
            self.entity.cargo.selected = 0
            self.entity.crew.selected = 0
            self.entity.broadsides.selected = 0
        else:
            self.engine.game_state = GameStates.PLAYER_DEAD
        return False
