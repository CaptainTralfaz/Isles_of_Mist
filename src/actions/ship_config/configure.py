from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base import Action
from actions.ship_config.exit_config import ExitConfigAction
from custom_exceptions import Impossible
from constants.enums import GameStates, MenuKeys, ShipConfig

if TYPE_CHECKING:
    from entity import Actor
    from enum import Enum


class ConfigureAction(Action):
    def __init__(self, entity: Actor, event: Enum, state: GameStates):
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
        if self.event in [MenuKeys.UP, ShipConfig.SAILS]:
            return False
        elif self.event in [MenuKeys.DOWN, ShipConfig.WEAPONS]:
            if self.state == GameStates.WEAPON_CONFIG:
                return ExitConfigAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.WEAPON_CONFIG
            return False
        elif self.event in [MenuKeys.LEFT, ShipConfig.CREW]:
            if self.state == GameStates.CREW_CONFIG:
                return ExitConfigAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.CREW_CONFIG
            return False
        elif self.event in [MenuKeys.RIGHT, ShipConfig.CARGO]:
            if self.state == GameStates.CARGO_CONFIG:
                return ExitConfigAction(self.entity).perform()
            else:
                self.engine.game_state = GameStates.CARGO_CONFIG
            return False
        raise Impossible(f"bad state {self.event}   wtf...")
