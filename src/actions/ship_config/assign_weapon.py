from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.ship_config.change_select import ChangeSelectionAction
from actions.ship_config.exit_config import ExitConfigAction
from constants.enums import Location, GameStates, MenuKeys
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class AssignWeaponAction(Action):
    def __init__(self, entity: Entity, event: Enum):
        """
        this action tries to assign (or remove) a weapon to/from a location, port or starboard
        :param entity: acting entity
        :param event: direction of assignment
        """
        super().__init__(entity)
        self.event = event
    
    def perform(self) -> bool:
        if not self.entity.is_alive:
            raise Impossible("Can't assign weapons when dead")
        if self.event in [MenuKeys.UP, MenuKeys.DOWN]:
            return ChangeSelectionAction(self.entity, self.event).perform()
        
        location, weapon = self.entity.broadsides.all_weapons[self.entity.broadsides.selected]
        if location in [Location.STORAGE]:
            if self.event == MenuKeys.LEFT and len(self.entity.broadsides.port) < self.entity.broadsides.slot_count:
                self.entity.broadsides.attach(location=Location.PORT, weapon=weapon)
                self.entity.broadsides.storage.remove(weapon)
                self.engine.message_log.add_message(f"Readied {weapon.name.capitalize()} to Port ")
                self.engine.game_state = GameStates.ACTION
                return ExitConfigAction(entity=self.entity, confirm=True).perform()
            elif self.event == MenuKeys.RIGHT \
                    and len(self.entity.broadsides.starboard) < self.entity.broadsides.slot_count:
                self.entity.broadsides.attach(location=Location.STARBOARD, weapon=weapon)
                self.entity.broadsides.storage.remove(weapon)
                self.engine.message_log.add_message(f"Readied {weapon.name.capitalize()} to Starboard ")
                self.engine.game_state = GameStates.ACTION
                return ExitConfigAction(entity=self.entity, confirm=True).perform()
        elif location in [Location.PORT]:
            if self.event == MenuKeys.LEFT:
                self.entity.broadsides.detach(weapon)
                self.engine.message_log.add_message(f"Removed {weapon.name.capitalize()} from Port ")
                self.engine.game_state = GameStates.ACTION
                return ExitConfigAction(entity=self.entity, confirm=True).perform()
        elif location in [Location.STARBOARD]:
            if self.event == MenuKeys.RIGHT:
                self.entity.broadsides.detach(weapon)
                self.engine.message_log.add_message(f"Removed {weapon.name.capitalize()} from Starboard ")
                self.engine.game_state = GameStates.ACTION
                return ExitConfigAction(entity=self.entity, confirm=True).perform()
        return False
