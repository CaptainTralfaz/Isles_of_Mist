from __future__ import annotations

from typing import TYPE_CHECKING

from actions.auto.salvage import SalvageAction
from actions.auto.wait import WaitAction
from actions.base.base import Action

if TYPE_CHECKING:
    from entity import Entity


class AutoAction(Action):
    def __init__(self, entity: Entity) -> None:
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
