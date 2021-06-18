from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.port.change_select import ChangeSelectionAction
from components.crew import occupation_stats
from constants.enums import MenuKeys

if TYPE_CHECKING:
    from entity import Entity


class TavernAction(Action):
    def __init__(self, entity: Entity, event: MenuKeys):
        """
        action for buying and selling while the player is in port
        :param entity: acting Entity
        """
        self.entity = entity
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        full_roster = []
        for crewman in self.entity.crew.roster:
            full_roster.append(crewman)
        for crewman in self.entity.game_map.port.tavern.roster:
            full_roster.append(crewman)
        selected = self.entity.crew.selected
        discount = 2 if self.entity.crew.has_occupation("captain") else 0
        
        roster = self.entity.crew.roster
        release_list = self.entity.crew.release_list
        hire_list = self.entity.crew.hire_list
        tavern = self.entity.game_map.port.tavern.roster
        
        if self.event == MenuKeys.UP:
            return ChangeSelectionAction(self.entity, self.event).perform()
        elif self.event == MenuKeys.DOWN:
            return ChangeSelectionAction(self.entity, self.event).perform()
        
        elif self.event == MenuKeys.LEFT:
            if full_roster[selected] in release_list:
                release_list.remove(full_roster[selected])
            elif full_roster[selected] in tavern and full_roster[selected] not in hire_list:
                hire_list.append(full_roster[selected])
                self.entity.game_map.port.tavern.temp_coins += \
                    occupation_stats[full_roster[selected].occupation]['cost'] - discount
            return False
        
        elif self.event == MenuKeys.RIGHT:
            if full_roster[selected] in hire_list:
                hire_list.remove(full_roster[selected])
                self.entity.game_map.port.tavern.temp_coins -= \
                    occupation_stats[full_roster[selected].occupation]['cost'] - discount
            elif full_roster[selected] in roster and full_roster[selected] not in release_list:
                release_list.append(full_roster[selected])
            return False
        
        return False
