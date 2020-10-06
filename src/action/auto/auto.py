from __future__ import annotations

from typing import TYPE_CHECKING

from action.auto.salvage import SalvageAction
from action.auto.wait import WaitAction
from action.base import Action

if TYPE_CHECKING:
    from entity import Actor


class AutoAction(Action):
    def __init__(self, entity: Actor) -> None:
        """
        This action directs what action should happen depending on the circumstances
            currently just salvage item or wait/coast
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        # make a decision on automatic action
        salvage = self.engine.game_map.get_items_at_location(self.entity.x, self.entity.y)
        if len(salvage) > 0:
            return SalvageAction(self.entity, salvage).perform()
        return WaitAction(self.entity).perform()