from __future__ import annotations

from typing import List, TYPE_CHECKING

from action.base import Action
from constants.colors import colors

if TYPE_CHECKING:
    from entity import Actor, Entity


class SalvageAction(Action):
    def __init__(self, entity: Actor, salvage: List[Entity]) -> None:
        """
        picks up all items in the entities location from the game map
        :param entity: acting Entity
        :param salvage: list of item entities to pick up
        """
        super().__init__(entity)
        self.salvage = salvage
    
    def perform(self) -> bool:
        for salvage in self.salvage:
            self.engine.message_log.add_message(f"You salvage {salvage.name}!", colors['orange'])
            self.entity.cargo.add_items_to_manifest(salvage.cargo.manifest)
            self.engine.game_map.entities.remove(salvage)
        return True
