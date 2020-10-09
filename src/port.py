from random import choice, randint
from typing import Dict, Tuple


class Port:
    def __init__(self,
                 location: Tuple[int, int] = (0, 0),
                 name: str = None,
                 merchant: Dict[str, int] = None,
                 smithy: Dict[str, int] = None):
        self.location = location
        self.name = name if name is name is not None else gen_port_name()
        self.merchant = merchant if merchant is not None else gen_merchant()
        self.smithy = smithy if smithy is not None else gen_smithy()

    def to_json(self) -> Dict:
        return {
            'location': self.location,
            'name': self.name,
            'merchant': self.merchant,
            'smithy': self.smithy
        }
    
    @staticmethod
    def from_json(json_data):
        location = json_data.get('location')
        name = json_data.get('name')
        merchant = json_data.get('merchant')
        smithy = json_data.get('smithy')
        return Port(location=location, name=name, merchant=merchant, smithy=smithy)
    

def gen_port_name() -> str:
    first = randint(0, 1)
    if first:
        adjective = choice([
            "Odd ", "Grand ", "Little ", "Poor ", "Tiny ", "Perfect ", "Stinky ", "Old ", "Fierce ", "Ole ", "Sad ",
            "Red ", "Black ", "Blue ", "Green ", "Yellow ", "Ugly ", "Rich ", "Happy ", "Royal ", "White ", "Drunken ",
            "Sandy ", "One ", "Sloppy ", "Tidy ", "Lonely ", "Deadly ", "Foggy ", "Big ", "Double ",
            "Shifty ", "Slippery ", "Hungry ", "Sliced ", "Oiled ", "Twisted ", "Long ", "Short ", "Crusty ",
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


def gen_merchant() -> Dict[str, int]:
    merchant = {}
    return merchant


def gen_smithy() -> Dict[str, int]:
    smithy = {}
    return smithy
