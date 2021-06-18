from __future__ import annotations

from random import choice, randint
from typing import Dict, Tuple

from components.crew import generate_roster
from port.smithy import Smithy
from port.merchant import Merchant
from port.tavern import Tavern


class Port:
    def __init__(self,
                 location: Tuple[int, int] = (0, 0),
                 name: str = None,
                 merchant: Merchant = None,
                 smithy: Smithy = None,
                 tavern: Tavern = None,
                 coins: int = None):
        self.location = location
        self.name = name if name is name is not None else gen_port_name()
        self.merchant = merchant if merchant is not None else Merchant()
        self.smithy = smithy if smithy is not None else Smithy()
        self.tavern = tavern if tavern is not None else Tavern()
        self.coins = coins if coins is not None else randint(100, 200)
        self.size = 1
    
    def to_json(self) -> Dict:
        return {
            'location': tuple(self.location),
            'name': self.name,
            'merchant': self.merchant.to_json(),
            'smithy': self.smithy.to_json(),
            'tavern': self.tavern.to_json(),
            'coins': self.coins,
        }
    
    @staticmethod
    def from_json(json_data):
        location_data = json_data.get('location')
        location = (location_data[0], location_data[1])
        name = json_data.get('name')
        merchant = Merchant.from_json(json_data.get('merchant'))
        smithy = Smithy.from_json(json_data.get('smithy'))
        tavern = Tavern.from_json(json_data.get('tavern'))
        coins = json_data.get('coins')
        return Port(location=location, name=name, merchant=merchant, smithy=smithy, tavern=tavern, coins=coins)

    def update_port(self):
        # for now, just divide up money from repairs and tavern between smithy / merchant
        print(f"Updating cargo/coins for {self.name}")
        self.merchant.coins += self.coins // 2
        self.smithy.coins += self.coins // 2
        print(f"{self.coins // 2} given to both Merchant and Tavern")
        # simulate next day's earnings base
        self.coins = randint(10, 20) * self.size
        self.tavern.roster.extend(generate_roster(randint(0, 2)))
        

def gen_port_name() -> str:
    first = randint(0, 1)
    if first:
        adjective = choice([
            "Odd ", "Grand ", "Little ", "Poor ", "Tiny ", "Perfect ", "Stinky ", "Old ", "Fierce ", "Ole ", "Sad ",
            "Red ", "Black ", "Blue ", "Green ", "Yellow ", "Ugly ", "Rich ", "Happy ", "Royal ", "White ", "Drunken ",
            "Sandy ", "One ", "Sloppy ", "Tidy ", "Lonely ", "Deadly ", "Foggy ", "Big ", "Double ", "Pierced ",
            "Slippery ", "Hungry ", "Sliced ", "Oiled ", "Twisted ", "Long ", "Short ", "Crusty ", "Shifty ",
            "Hairy ", "New ", "Jolly ", "Half ", "Dirty ", "Salty ", "Tired ", "Lumpy ", "Leaning ", "Round ", "Bad ",
            "Angry ", "Ancient ", "Zero ", "Lame ", "Fancy ", "Priceless ", "Worthless ", "Lazy ", "Rocky ",
            "Windy ", "Dry ", "Sunny ", "Hazy ", "Shady "
        ])
    else:
        adjective = ""
    name = choice([
        "Parrot", "Sugar", "Rum", "Sand", "Coral", "Booty", "Danger", "Bad", "Jungle", "Shark", "Rat", "Hag", "Gold",
        "Bone", "Skull", "Finger", "Knuckle", "Dragon", "Serpent", "Turtle", "Mermaid", "Wyvern", "Corpse", "Gallows",
        "Jester", "Pearl", "Rock", "Sailor", "Captain", "Spice", "Uncle", "Fish", "Orphan", "Ogre", "Brick", "Copper",
        "Spider", "Coconut", "Gull", "Coin", "Cannon", "Anchor", "Tar", "Cutlass", "Monkey", "Boy", "Golem", "Silver",
        "Blood", "Bottle", "Jug", "Tankard", "Storm", "Cloud", "Spray", "Tide", "Witch", "Beggar", "Maiden", "Iron",
        "Banana", "Doom", "Voodoo", "Pirate", "Fever", "Stone", "Wood", "Raider", "Boar", "Heart", "Salt", "Obsidian"
    ])
    if first:
        second = randint(0, 1)
    else:
        second = 1
    if second or not first:
        postfix = choice([
            " Harbor", " Hook", " Bay", " Town", " Hole", " Inlet", " Twist", " Jetty", " Wharf", " Quay", " Narrows",
            " Fort", " Cape", " Shire", " Cabin", " Hut", " Place", " Fork", " Pier", " Village", " Camp", " Island",
            " Beach", " Coast", " Cavern", " Copse", " Cave", " Slip", " Landing", " Clearing", " Shoals", " Shakes",
            " Shore", " Bar", " Straight", " Dock", " Boom", " Tip", " Leg", " Haven", " Marina", " Mooring", " Dunes",
            "ville", "town", " Spot", " Dock", " Isle", " Ferry", " Dream", " Home", " Point", " Pit", " Post", " Horn"
        ])
    else:
        postfix = ""
    possessive = ""
    if len(postfix) > 0:
        if postfix.startswith(" ") and not randint(0, 3):
            possessive = "'s"
    return f"port {adjective}{name}{possessive}{postfix}"
