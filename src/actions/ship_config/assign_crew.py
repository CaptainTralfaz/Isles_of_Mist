from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.ship_config.exit_config import ExitConfigAction
from constants.enums import GameStates
from constants.stats import occupation_stats
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity
    from enum import Enum


class AssignCrewAction(Action):
    def __init__(self, entity: Entity, event: Enum):
        """
        "assigns" selected crewman to a directional button
        :param entity: acting Entity
        :param event: direction key assigning crew to
        """
        super().__init__(entity)
        self.event = event
    
    def perform(self) -> bool:
        if not self.entity.is_alive:
            raise Impossible("Can't assign crew when dead")
        
        crewman = self.entity.crew.roster[self.entity.crew.selected]
        
        # if crewman already has this assignment, then un-assign him
        if crewman.assignment == self.event:
            crewman.assignment = None
            self.engine.message_log.add_message(f"Assigning nobody to the '{self.event.name}' key")
            return ExitConfigAction(entity=self.entity).perform()
        else:
            if occupation_stats[crewman.occupation]['cd'] == 0:
                raise Impossible(f"A {crewman.occupation.capitalize()} cannot be assigned special duties")
            # remove other assigned crewman
            for person in self.entity.crew.roster:
                if person.assignment == self.event:
                    person.assignment = None
            crewman.assignment = self.event
            crewman.cooldown = crewman.cooldown_max
            self.engine.message_log.add_message(f"Assigning {crewman.name} the {crewman.occupation.capitalize()}"
                                                f" to the '{self.event.name}' key")
            self.engine.game_state = GameStates.ACTION
            return ExitConfigAction(entity=self.entity, confirm=True).perform()
