from __future__ import annotations

from typing import List, TYPE_CHECKING

from actions.base.base import Action

if TYPE_CHECKING:
    from entity import Entity


class SalvageAction(Action):
    def __init__(self, entity: Entity, salvage: List[Entity]) -> None:
        """
        picks up all items in the entities location from the game map
        :param entity: acting Entity
        :param salvage: list of item entities to pick up
        """
        super().__init__(entity)
        self.salvage = salvage
    
    def perform(self) -> bool:
        for salvage in self.salvage:
            self.engine.message_log.add_message(f"You salvage {salvage.name}!", text_color='orange')
            self.entity.cargo.add_coins_to_cargo(salvage.cargo.coins)
            self.entity.cargo.add_items_to_manifest(salvage.cargo.manifest)
            self.engine.game_map.entities.remove(salvage)
        return True
