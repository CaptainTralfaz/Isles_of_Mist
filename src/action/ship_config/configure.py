from __future__ import annotations

from typing import TYPE_CHECKING

from action.base import Action
from action.ship_config.exit import ExitMenuAction
from custom_exceptions import Impossible
from constants.enums import GameStates

if TYPE_CHECKING:
    from entity import Actor


class ConfigureAction(Action):
    def __init__(self, entity: Actor, event: str, state: GameStates):
        """
        directs which action to use when in the configuration menus
        :param entity: acting Entity
        :param event:
        :param state: GameState
        """
        self.event = event
        self.state = state
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event in ["up", "sails"]:
            return False
        elif self.event in ["down", "weapons"]:
            if self.state == GameStates.WEAPON_CONFIG:
                return ExitMenuAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.WEAPON_CONFIG
            return False
        elif self.event in ["left", "crew"]:
            if self.state == GameStates.CREW_CONFIG:
                return ExitMenuAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.CREW_CONFIG
            return False
        elif self.event in ["right", "cargo"]:
            if self.state == GameStates.CARGO_CONFIG:
                return ExitMenuAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.CARGO_CONFIG
            return False
        raise Impossible(f"bad state {self.event}   wtf...")
