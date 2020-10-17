from random import randint
from typing import List

from components.crew import Crewman, generate_roster


class Tavern:
    def __init__(self, roster: List = None):
        self.temp_coins = 0
        self.roster = roster if roster is not None else generate_roster(randint(10, 15))
    
    def to_json(self):
        return {
            'roster': [crewman.to_json() for crewman in self.roster]
        }
    
    @staticmethod
    def from_json(json_data):
        roster_data = json_data.get('roster')
        return Tavern(roster=[Crewman.from_json(crewman) for crewman in roster_data])
