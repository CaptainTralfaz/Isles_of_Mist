from __future__ import annotations

from typing import TYPE_CHECKING

from action.base import Action
from action.ship_config.assign_crew import AssignCrewAction
from action.ship_config.assign_weapon import AssignWeaponAction
from enums import GameStates

if TYPE_CHECKING:
    from entity import Actor


class SelectedAction(Action):
    def __init__(self, entity: Actor, event: str, state: GameStates):
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
        print(f"moving selection {self.event}")
        return False
