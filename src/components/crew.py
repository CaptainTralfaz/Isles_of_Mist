from __future__ import annotations

from random import choice, randint
from typing import List, Dict, TYPE_CHECKING

from components.base import BaseComponent
from constants.constants import move_elevations
from constants.enums import GameStates, RenderOrder, MenuKeys
from event_handlers.player_dead import GameOverEventHandler
from utilities import choice_from_dict

if TYPE_CHECKING:
    from entity import Entity

starting_crew_list = ["lookout", "archer", "sharpshooter", "sailor", "sailor", "sailor",
                      "shipwright", "tailor", "cook", "captain"]


class Crew(BaseComponent):
    parent: Entity
    
    def __init__(self,
                 max_count: int,
                 defense: int,
                 name: str = "crew",
                 roster: List = None) -> None:
        self.max_count = max_count
        self.defense = defense
        self.name = name
        self.roster = roster
        if self.roster is None:
            self.roster = generate_new_game_roster(starting_crew_list)
        self.selected = 0
        self.release_list = []
        self.hire_list = []
    
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
        roster = [Crewman.from_json(crewman) for crewman in roster_list]
        return Crew(max_count=max_count, defense=defense, roster=roster)
    
    @property
    def weight(self):
        """
        Determines total weight of crew
        :return: total weight of crew
        """
        return len(self.roster) * 20
    
    @property
    def volume(self):
        """
        Determines total volume of crew
        :return: total volume of crew
        """
        return len(self.roster) * 20
    
    def has_occupation(self, occupation: str) -> bool:
        for crewman in self.roster:
            if crewman.occupation == occupation:
                return True
        return False
    
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
        new_crew_value = len(self.roster) + amount
        if new_crew_value > self.max_count:
            new_crew_value = self.max_count
        amount_hired = new_crew_value - len(self.roster)
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
            if len(self.roster) <= 0:
                self.die()


def generate_roster(count: int):
    roster = []
    for crewman in range(count):
        roster.append(Crewman())
    return roster


def generate_new_game_roster(occupation_list):
    roster = []
    for occupation in occupation_list:
        roster.append(Crewman(occupation=occupation))
    return roster


class Crewman:
    def __init__(self, name: str = None, occupation: str = None, assignment: MenuKeys = None):
        self.name = self.generate_name() if name is None else name
        self.occupation = self.generate_occupation() if occupation is None else occupation
        self.assignment = assignment
        self.cooldown = 0
        self.cooldown_max = occupation_stats[self.occupation]['cd']
    
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
        nickname = ""
        if randint(0, 5) == 0:
            nickname = choice([
                "'Fat' ", "'Skinny' ", "'Lazy' ", "'Big' ", "'Tiny' ", "'Old' ", "'Young' ", "'Handsome' ", "'Stinky' ",
                "'Lucky' ", "'Dark' ", "'Pale' ", "'Crazy' ", "'Sharp' ", "'Mean' ", "'Smelly' ", "'Drunk'", "'Tipsy' ",
                "'Sleepy' ", "'Lumpy' ", "'Bald' ", "'Quick' ", "'Fancy' ", "'Ugly' ", "'Long' ", "'Wise' ", "'Rusty' ",
                "'Sneaky' ", "'Honest' ", "'Dirty' ", "'Clumsy' ", "'Slippery' ", "'Fierce' ", "'Mighty' ", "'Pretty' ",
                "'Quiet' ", "'Eagle Eye' ", "'Cautious' ", "'Hairy' ", "'Cruel' ", "'Angry' ", "'Salty' ", "'Crusty' ",
                "'Slim' ", "'Wild' ", "'Poor' ", "'Thrifty' ",
            ])
        first = choice([
            "Jack", "James", "Benjamin", "Halsten", "Joseph", "Phillip", "Robert", "Carey", "Terrance", "Igor", "Derek",
            "Stephen", "Russel", "Sherman", "Kenneth", "Alexander", "Thomas", "Albert", "Paddington", "Roger", "Arthur",
            "Samuel", "Shaun", "Sean", "Andrew", "Marcus", "Daniel", "Christopher", "David", "Michael", "Bryan", "Evan",
            "Percival", "Louis", "Edward", "Silas", "Timothy", "Abraham", "Eric", "Lief", "Nicholas", "Braxton", "Adam",
            "Harold", "Harrison", "Dennis", "Darrel", "Raymond", "Cornelius", "Charles", "Steffan", "Raymond", "Lucas",
            "Virgil", "Orville", "Gerald", "Vance", "Stanley", "Darren", "Ingvar", "Royce", "Harold", "Linus", "Gordon",
            "Bradley", "Patrick", "Calvin", "Matthew", "Jonas", "Bertram", "Isaac", "Miles", "Wendel", "Rene", "Ronald",
            "George", "Joshua", "Martin", "Justin", "Bruce", "Zachary", "Brandon", "Carlton", "Lance", "Randal", "Paul",
            "Julius", "Augustus", "Curtis", "Gregory", "Forrest", "Oliver", "Donavan", "Jonathon", "Octavius", "Conrad",
            "Brutus", "Emeryl", "Ernest", "Richard", "Trevor", "Noah", "Reginald", "Aaron", "Malcolm", "Pierre", "Amos",
            "Henry", "Douglas", "Theodore", "Francis", "Fredrick", "Peter", "Felix", "Duane", "Joel", "Byron", "Kellen",
            "Ian", "Grant",
        ])
        last = choice([
            "Jones", "Bones", "Smith", "Sparrow", "Turner", "Silver", "Corday", "Conroy", "Evans", "Maxwell", "Jameson",
            "Finch", "Smythe", "Harrison", "Harris", "Black", "Ramsey", "Gray", "Carpenter", "Fisher", "Lewis", "Adams",
            "Archer", "Quinn", "Wylde", "Robbins", "Hawkins", "Pierce", "Anderson", "Quimby", "Dance", "James", "Flint",
            "Hunter", "Beck", "Beckett", "Peck", "Samson", "Porter", "Gibbs", "Dalton", "Chase", "Avery", "Aims", "Ott",
            "Sherman", "Sheridan", "Ford", "Nelson", "Baldwin", "Woods", "Edwards", "Erikson", "Ferris", "Oaks", "Tate",
            "Young", "Flynn", "Beard", "Sharpe", "Bonds", "Dickerson", "Dickens", "White", "Brown", "Iverson", "Warner",
            "Thomas", "Thomson", "Hamm", "Abrams", "Hammond", "Philips", "Jensen", "Johnson", "Mercy", "Miles", "Scott",
            "Oatley", "Bryant", "Caldwell", "Chisolm", "Goode", "DuMorne", "Early", "Nance", "Nevins", "Park", "Parker",
            "Royce", "Irving", "Vale", "Valley", "York", "Dunn", "Holden", "Xavier", "Paris", "Parish", "Ogden", "Pyre",
            "Davidson", "Benson", "Davis", "Price", "Stone", "Hobbs", "Cobb", "Harrington", "Foster", "Wright", "Green",
            "Cavanaugh", "Mannish", "Landry", "Cavandish", "Scott", "Snelling", "Richards", "Towers", "Barton", "Stowe",
            "Lincoln", "Harris", "Morgan", "Starling", "Miller", "Quince", "Oswald", "Peterson", "Pine", "Hale", "Ward",
            "Flemming", "MacDonald", "McCray", "Downs", "Ivy", "Scrubbs", "Sneed", "Morris", "Morrison", "Sands", "Sty",
            "Stay", "Steel", "McNee", "Maine", "Decker", "Moore", "Riley", "Shilling",
        ])
        return f"{nickname}{first} {last}"
    
    @staticmethod
    def generate_occupation():
        return choice_from_dict({
            "sailor": 80,
            "cook": 5,
            "soldier": 5,
            "archer": 10,  # added
            "rogue": 10,
            "fisherman": 15,
            "lookout": 10,  # added
            "captain": 5,
            "tailor": 5,
            "shipwright": 5,
            "engineer": 5,
            "sharpshooter": 5,  # added
            "mistweaver": 1,
            "seer": 5,
            "diver": 5,
            "scryer": 1,
            "steward": 5,
            "smith": 5,
            "stormbringer": 1,
            "surgeon": 1,
        })


# TODO move to constants.stats
""" maps occupation to cooldown_max"""
occupation_stats = {
    "cook": {
        'cd': 0,
        'cost': 10,
    },  # Auto: feed crew extra somehow OR Action: reduce other crew cooldowns ?
    "soldier": {
        'cd': 0,
        'cost': 12,
    },  # Auto: +1 crew defense vs melee? but dies first...
    "sailor": {
        'cd': 0,
        'cost': 8,
    },
    "archer": {
        'cd': 0,
        'cost': 12,
    },  # Auto: +1 damage to arrow total
    "sharpshooter": {
        'cd': 0,
        'cost': 13,
    },  # Auto: + 1 weapon damage total
    "lookout": {
        'cd': 0,
        'cost': 12,
    },  # Auto: + 1 view
    "rogue": {
        'cd': 0,
        'cost': 9,
    },
    "fisherman": {
        'cd': 5,
        'cost': 6,
    },  # Action: catches fish at seaweed
    "captain": {
        'cd': 0,
        'cost': 15,
    },  # Auto: raises morale
    "shipwright": {
        'cd': 5,
        'cost': 13,
    },  # Action: repairs ship with tar & wood
    "engineer": {
        'cd': 5,
        'cost': 13,
    },  # Action: repairs ballista with rope and wood
    "mistweaver": {
        'cd': 5,
        'cost': 15,
    },  # Action: summons a circle of mist around ship
    "seer": {
        'cd': 5,
        'cost': 11,
    },  # Action: reveal terrain no LOS blocking
    "tailor": {
        'cd': 5,
        'cost': 12,
    },  # Action: repair sails with rope and canvas
    "scryer": {
        'cd': 10,
        'cost': 13,
    },  # Action: reveals location of all monsters in viewport
    "smith": {
        'cd': 5,
        'cost': 12,
    },  # Action: repair cannons with iron
    "stormbringer": {
        'cd': 10,
        'cost': 14,
    },  # Action: makes weather worse
    "diver": {
        'cd': 0,
        'cost': 9,
    },  # Auto: recover more from sunken ships?
    "steward": {
        'cd': 0,
        'cost': 12,
    },  # fit more cargo somehow? - maybe keep cargo from being damaged / washing overboard?
    "surgeon": {
        'cd': 0,
        'cost': 14,
    },  # ?
    "minstrel": {
        'cd': 0,
        'cost': 10,
    },  # reduce max cooldowns of others by 1 ?
    "merchant": {
        'cd': 0,
        'cost': 12,
    },  # Auto: discount buying/selling
    "cartographer": {
        'cd': 0,
        'cost': 12,
    },  # Auto: allows reading of maps
}
