from __future__ import annotations

from typing import TYPE_CHECKING

from actions.attack.arrow import ArrowAction
from actions.attack.broadsides import BroadsideAction
from actions.attack.mine import MineAction
from actions.base.base import Action
from constants.enums import Location

if TYPE_CHECKING:
    from entity import Actor


class AttackAction(Action):
    def __init__(self, entity: Actor, direction: Location):
        """
        this action directs which action should be used to make an attack, depending on the direction
        :param entity: acting Entity
        :param direction: the key pressed for the attack
        """
        super().__init__(entity)
        self.direction = direction
    
    def perform(self) -> bool:
        if self.direction in [Location.PORT, Location.STARBOARD]:
            return BroadsideAction(self.entity, self.direction).perform()
        if self.direction in [Location.FORE]:
            return ArrowAction(self.entity, self.direction).perform()
        if self.direction in [Location.AFT]:
            return MineAction(self.entity).perform()
        return False
