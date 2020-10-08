from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.repair.hire_crew import HireCrewAction
from actions.repair.hull import RepairHullAction
from actions.repair.sails import RepairSailsAction
from actions.repair.weapons import RepairWeaponsAction

if TYPE_CHECKING:
    from entity import Actor


class RepairAction(Action):
    def __init__(self, entity: Actor, event: str):
        """
        this action directs which action should be used during a repair action
        :param entity: acting entity
        :param event: flag directing the action
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.event == "crew":
            return HireCrewAction(self.entity).perform()
        if self.event == "sails":
            return RepairSailsAction(self.entity).perform()
        if self.event == "shipyard":
            return RepairHullAction(self.entity).perform()
        if self.event == "engineer":
            return RepairWeaponsAction(self.entity).perform()
