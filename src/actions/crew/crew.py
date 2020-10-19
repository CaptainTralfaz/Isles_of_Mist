from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base.base import Action
from actions.crew.cook import Cook
from actions.crew.engineer import Engineer
from actions.crew.fisherman import Fisherman
from actions.crew.mistweaver import MistWeaver
from actions.crew.scryer import Scryer
from actions.crew.seer import Seer
from actions.crew.shipwright import Shipwright
from actions.crew.smith import Smith
from actions.crew.stormbringer import StormBringer
from actions.crew.stormcalmer import StormCalmer
from actions.crew.tailor import Tailor
from actions.crew.windsoother import WindSoother
from actions.crew.windcaller import WindCaller
from constants.enums import MenuKeys
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Entity

action_lookup = {
    "shipwright": Shipwright,
    "tailor": Tailor,
    "engineer": Engineer,
    "mistweaver": MistWeaver,
    "windsoother": WindSoother,
    "windcaller": WindCaller,
    "stormbringer": StormBringer,
    "stormcalmer": StormCalmer,
    "cook": Cook,
    "seer": Seer,
    "scryer": Scryer,
    "smith": Smith,
    "fisherman": Fisherman,
}


class CrewAction(Action):
    def __init__(self, entity: Entity, event: MenuKeys):
        """
        this action directs which action should be used when attempting a Crewman Occupation action
        :param entity: acting Entity
        :param event: the key pressed
        """
        self.event = event
        super().__init__(entity)
    
    def perform(self) -> bool:
        action = None
        assigned = None
        for crewman in self.entity.crew.roster:
            if crewman.assignment and crewman.assignment == self.event:
                assigned = crewman
                action = action_lookup[crewman.occupation]
        if action and assigned:
            return action(self.entity, assigned).perform()
        else:
            raise Impossible(f"Nobody assigned to '{self.event.name.upper()}' key")
