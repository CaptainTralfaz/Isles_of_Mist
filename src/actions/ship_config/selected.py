from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.ship_config.assign_crew import AssignCrewAction
from actions.ship_config.assign_weapon import AssignWeaponAction
from actions.ship_config.drop_cargo import DropCargoAction
from constants.enums import GameStates

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class SelectedAction(Action):
    def __init__(self, entity: Entity, event: Enum, state: GameStates):
        """
        this action directs which action should be used when the highlighted item in a list is
            selected for another action
        :param entity: acting Entity
        :param event: the event taking place
        :param state: GameState
        """
        self.event = event
        self.state = state
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.state == GameStates.CREW_CONFIG:
            return AssignCrewAction(self.entity, self.event).perform()
        if self.state == GameStates.WEAPON_CONFIG:
            return AssignWeaponAction(self.entity, self.event, self.state).perform()
        if self.state == GameStates.CARGO_CONFIG:
            return DropCargoAction(self.entity, self.event).perform()
        return False
