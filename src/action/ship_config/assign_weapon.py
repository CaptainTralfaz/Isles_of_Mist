from __future__ import annotations

from typing import TYPE_CHECKING

from action.base import Action
from action.ship_config.change_select import ChangeSelectionAction
from custom_exceptions import Impossible
from constants.enums import Location, GameStates

if TYPE_CHECKING:
    from entity import Actor


class AssignWeaponAction(Action):
    def __init__(self, entity: Actor, event: str, state: GameStates):
        """
        this action tries to assign (or remove) a weapon to/from a location, port or starboard
        :param entity: acting entity
        :param event: direction of assignment
        :param state: GameState
        """
        super().__init__(entity)
        self.event = event
        self.state = state
    
    def perform(self) -> bool:
        if not self.entity.is_alive:
            raise Impossible("Can't assign weapons when dead")
        if self.event in ["up", "down"]:
            return ChangeSelectionAction(self.entity, self.event, self.state).perform()
        
        location, weapon = self.entity.broadsides.all_weapons[self.entity.broadsides.selected]
        if location in ["storage"]:
            if self.event == "left" and len(self.entity.broadsides.port) < self.entity.broadsides.slot_count:
                self.entity.broadsides.attach(location=Location.PORT, weapon=weapon)
                self.entity.broadsides.storage.remove(weapon)
                self.engine.message_log.add_message(f"Readied {weapon.name.capitalize()} to Port ")
                self.engine.game_state = GameStates.ACTION
                return True
            elif self.event == "right" and len(self.entity.broadsides.starboard) < self.entity.broadsides.slot_count:
                self.entity.broadsides.attach(location=Location.STARBOARD, weapon=weapon)
                self.entity.broadsides.storage.remove(weapon)
                self.engine.message_log.add_message(f"Readied {weapon.name.capitalize()} to Starboard ")
                self.engine.game_state = GameStates.ACTION
                return True
        elif location in [Location.PORT]:
            if self.event == "left":
                self.entity.broadsides.detach(weapon)
                self.engine.message_log.add_message(f"Removed {weapon.name.capitalize()} from Port ")
                self.engine.game_state = GameStates.ACTION
                return True
        elif location in [Location.STARBOARD]:
            if self.event == "right":
                self.entity.broadsides.detach(weapon)
                self.engine.message_log.add_message(f"Removed {weapon.name.capitalize()} from Starboard ")
                self.engine.game_state = GameStates.ACTION
                return True
        return False
