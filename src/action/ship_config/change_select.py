from __future__ import annotations

from typing import TYPE_CHECKING

from action.base import Action
from custom_exceptions import Impossible
from enums import GameStates

if TYPE_CHECKING:
    from entity import Actor


class ChangeSelectionAction(Action):
    def __init__(self, entity: Actor, event: str, state: GameStates):
        """
        this action moves the selector up or down in the config menus
        :param entity: acting Entity
        :param event: the key pressed
        :param state: GameState
        """
        self.event = event
        self.state = state
        super().__init__(entity)
    
    def perform(self) -> bool:
        if self.state == GameStates.WEAPON_CONFIG:
            component = self.entity.broadsides
            length = len(self.entity.broadsides.all_weapons) - 1
        elif self.state == GameStates.CARGO_CONFIG:
            component = self.entity.cargo
            length = len(self.entity.cargo.manifest.keys()) - 1
        elif self.state == GameStates.CREW_CONFIG:
            component = self.entity.crew
            length = len(self.entity.crew.roster) - 1
        else:
            raise Impossible("Bad State")
        
        if self.event == "up":
            component.selected -= 1
            if component.selected < 0:
                component.selected = length
        if self.event == "down":
            component.selected += 1
            if component.selected > length:
                component.selected = 0
        return False
