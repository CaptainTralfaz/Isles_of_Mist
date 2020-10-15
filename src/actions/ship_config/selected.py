from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.ship_config.assign_crew import AssignCrewAction
from actions.ship_config.assign_weapon import AssignWeaponAction
from actions.ship_config.assign_cargo import AssignCargoAction
from constants.enums import GameStates

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class SelectedAction(Action):
    def __init__(self, entity: Entity, event: Enum):
        """
        this action directs which action should be used when the highlighted item in a list is
            selected for another action
        :param entity: acting Entity
        :param event: the event taking place
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.entity.game_map.engine.game_state == GameStates.CREW_CONFIG:
            self.entity.cargo.sell_list = {}
            return AssignCrewAction(self.entity, self.event).perform()
        if self.entity.game_map.engine.game_state == GameStates.WEAPON_CONFIG:
            self.entity.cargo.sell_list = {}
            return AssignWeaponAction(self.entity, self.event).perform()
        if self.entity.game_map.engine.game_state == GameStates.CARGO_CONFIG:
            return AssignCargoAction(self.entity, self.event).perform()
        return False
