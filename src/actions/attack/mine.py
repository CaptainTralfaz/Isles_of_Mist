from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity


class MineAction(Action):
    def __init__(self, entity: Entity):
        """
        creates a Minefield decoration on the game map
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        if not self.entity.cargo.item_type_in_manifest('mines'):
            raise Impossible("No mines in inventory!")
        self.engine.game_map.terrain[self.entity.x][self.entity.y].decoration = "minefield"
        self.entity.cargo.remove_items_from_manifest({'mines': 1})
        self.engine.message_log.add_message("Mines placed")
        return True
