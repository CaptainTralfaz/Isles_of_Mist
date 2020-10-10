from __future__ import annotations

from random import choice
from typing import List, Dict, TYPE_CHECKING

from components.base import BaseComponent
from constants.constants import move_elevations
from constants.enums import GameStates, RenderOrder, MenuKeys
from event_handlers.player_dead import GameOverEventHandler
from utilities import choice_from_dict

if TYPE_CHECKING:
    from entity import Entity


class Crew(BaseComponent):
    parent: Entity
    
    def __init__(self,
                 count: int,  # TODO remove this, use len(roster)
                 max_count: int,
                 defense: int,
                 name: str = "crew",
                 roster: List = None) -> None:
        self.max_count = max_count
        self._count = count
        self.defense = defense
        self.name = name
        self.roster = roster
        if self.roster is None:
            self.roster = generate_roster(max_count)
        self.selected = 0
    
    def to_json(self) -> Dict:
        """
        Serialize Crew object to json
        :return: json representation of Crew object
        """
        return {
            'max_count': self.max_count,
            'defense': self.defense,
            'roster': [crewman.to_json() for crewman in self.roster],
        }
    
    @staticmethod
    def from_json(json_data) -> Crew:
        """
        Convert json representation Crew object to Crew Object
        :param json_data: json representation of Crew object
        :return: Crew Object
        """
        max_count = json_data.get('max_count')
        defense = json_data.get('defense')
        roster_list = json_data.get('roster')
        count = len(roster_list)
        roster = [Crewman.from_json(crewman) for crewman in roster_list]
        return Crew(count=count, max_count=max_count, defense=defense, roster=roster)
    
    @property
    def weight(self):
        """
        Determines total weight of crew
        :return: total weight of crew
        """
        return self.count * 75
    
    @property
    def volume(self):
        """
        Determines total volume of crew
        :return: total volume of crew
        """
        return self.count * 75
    
    @property
    def count(self) -> int:
        return self._count
    
    @count.setter
    def count(self, value: int) -> None:
        self._count = max(0, min(value, self.max_count))
        if self._count == 0 and self.parent.ai:
            self.die()
    
    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "All your crew belong to the sea! Game Over!"
            self.parent.icon = "shipwreck"
            self.engine.event_handler = GameOverEventHandler(self.engine)
            self.engine.game_state = GameStates.PLAYER_DEAD
            death_message_color = 'red'
        else:
            death_message = f"{self.parent.name} has no crew left!"
            if self.game_map.terrain[self.parent.x][self.parent.y].elevation in move_elevations["water"]:
                self.parent.icon = "carcass"
            else:
                self.parent.icon = None
            death_message_color = 'orange'
        
        self.parent.facing = 0
        self.parent.ai = None
        self.parent.name = f"{self.parent.name} Corpse"
        self.parent.render_order = RenderOrder.CORPSE
        self.parent.view.distance = 0
        self.parent.flying = False
        self.engine.message_log.add_message(death_message, text_color=death_message_color)
    
    def hire(self, amount: int) -> int:
        new_crew_value = self.count + amount
        if new_crew_value > self.max_count:
            new_crew_value = self.max_count
        amount_hired = new_crew_value - self.count
        self.count = new_crew_value
        for crew in range(amount_hired):
            crewman = Crewman()
            self.roster.append(crewman)
            self.engine.message_log.add_message(f"Hired {crewman.name} the {crewman.occupation}",
                                                text_color='cyan')
        return amount_hired
    
    def take_damage(self, amount: int) -> None:
        for crew in range(amount):
            if len(self.roster) > 0:
                # pick a crewman
                pick = choice(self.roster)
                self.engine.message_log.add_message(f"{pick.name} the {pick.occupation} has perished!",
                                                    text_color='orange')
                # kill crewman
                self.roster.remove(pick)
        self.count -= amount


def generate_roster(count: int):
    roster = []
    for crewman in range(count):
        roster.append(Crewman())
    return roster


class Crewman:
    def __init__(self, name: str = None, occupation: str = None, assignment: MenuKeys = None):
        self.name = self.generate_name() if name is None else name
        self.occupation = self.generate_occupation() if occupation is None else occupation
        self.assignment = assignment
    
    def to_json(self) -> Dict:
        return {
            'name': self.name,
            'occupation': self.occupation,
            'assignment': self.assignment.value if self.assignment is not None else None
        }
    
    @staticmethod
    def from_json(json_data) -> Crewman:
        name = json_data.get('name')
        occupation = json_data.get('occupation')
        assignment_data = json_data.get('assignment')
        assignment = None
        if assignment_data is not None:
            assignment = MenuKeys(assignment_data)
        return Crewman(name=name, occupation=occupation,
                       assignment=assignment)
    
    @staticmethod
    def generate_name():
        first = choice(["Jim", "Billy", "Sam", "Jack", "Davey", "Mick", "Alex"])
        last = choice(["Jones", "Bones", "Tate", "Sparrow", "Turner", "Silver", "Corday", "Conroy"])
        return f"{first} {last}"
    
    @staticmethod
    def generate_occupation():
        return choice_from_dict({"sailor": 90,
                                 "cook": 10,
                                 "soldier": 5,
                                 "archer": 10,
                                 "rogue": 10,
                                 "captain": 5,
                                 "farmer": 5,
                                 "carpenter": 5,
                                 "engineer": 5,
                                 "sharpshooter": 5,
                                 "mistweaver": 1,
                                 "seer": 5,
                                 "diver": 5,
                                 "scryer": 1,
                                 "steward": 5,
                                 "smith": 5,
                                 "stormbringer": 1,
                                 "surgeon": 1,
                                 })
