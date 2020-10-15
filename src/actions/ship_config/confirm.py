from __future__ import annotations

from typing import Optional, Dict, TYPE_CHECKING

from actions.base.base import Action
from actions.ship_config.exit_config import ExitConfigAction
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
        elif self.event in [MenuKeys.UP, MenuKeys.DOWN]:
            return False
        elif self.event == MenuKeys.LEFT:
            return ExitConfigAction(self.entity).perform()
        else:
            return ExitConfigAction(self.entity, confirm=True).perform()
