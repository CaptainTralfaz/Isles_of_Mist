from __future__ import annotations

from random import choice, randint
from typing import Dict, Tuple, List

from constants.constants import MERCHANT, SMITHY
from utilities import choice_from_dict
from components.weapon import Weapon


class Port:
    def __init__(self,
                 location: Tuple[int, int] = (0, 0),
                 name: str = None,
                 merchant: Merchant = None,
                 smithy: Smithy = None):
        self.location = location
        self.name = name if name is name is not None else gen_port_name()
        self.merchant = merchant if merchant is not None else Merchant()
        self.smithy = smithy if smithy is not None else Smithy()
    
    def to_json(self) -> Dict:
        return {
            'location': tuple(self.location),
            'name': self.name,
            'merchant': self.merchant.to_json(),
            'smithy': self.smithy.to_json()
        }
    
    @staticmethod
    def from_json(json_data):
        location_data = json_data.get('location')
        location = (location_data[0], location_data[1])
        name = json_data.get('name')
        merchant = Merchant.from_json(json_data.get('merchant'))
        smithy = Smithy.from_json(json_data.get('smithy'))
        return Port(location=location, name=name, merchant=merchant, smithy=smithy)


def gen_port_name() -> str:
    first = randint(0, 1)
    if first:
        adjective = choice([
            "Odd ", "Grand ", "Little ", "Poor ", "Tiny ", "Perfect ", "Stinky ", "Old ", "Fierce ", "Ole ", "Sad ",
            "Red ", "Black ", "Blue ", "Green ", "Yellow ", "Ugly ", "Rich ", "Happy ", "Royal ", "White ", "Drunken ",
            "Sandy ", "One ", "Sloppy ", "Tidy ", "Lonely ", "Deadly ", "Foggy ", "Big ", "Double ", "Pierced "
                                                                                                     "Shifty ",
            "Slippery ", "Hungry ", "Sliced ", "Oiled ", "Twisted ", "Long ", "Short ", "Crusty ",
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


class Merchant:
    def __init__(self, manifest: Dict = None, coins: int = None):
        self.coins = coins if coins is not None else randint(200, 300)
        self.temp_coins = 0
        # TODO generate this depending on port's surroundings / buildings
        #  but for now...
        if manifest is not None:
            self.manifest = manifest
        else:
            self.manifest = {}
            for x in range(0, randint(100, 200)):
                pick = choice_from_dict(MERCHANT)
                if pick in self.manifest.keys():
                    self.manifest[pick] += 1
                else:
                    self.manifest[pick] = 1
    
    def to_json(self):
        return {'coins': self.coins,
                'manifest': self.manifest}
    
    @staticmethod
    def from_json(json_data):
        return Merchant(manifest=json_data.get('manifest'), coins=json_data.get('coins'))


class Smithy:
    def __init__(self, manifest: List[Weapon] = None, coins: int = None):
        # TODO generate this depending on port's surroundings / buildings
        #  but for now...
        self.coins = coins if coins is not None else randint(50, 100)
        self.temp_coins = 0
        if manifest is not None:
            self.manifest = manifest
        else:
            self.manifest = []
            for x in range(0, randint(2, 3)):
                self.manifest.append(Weapon.make_weapon_from_name(choice_from_dict(SMITHY)))
    
    def to_json(self):
        return {'coins': self.coins,
                'manifest': [weapon.to_json() for weapon in self.manifest]}
    
    @staticmethod
    def from_json(json_data):
        manifest_data = json_data.get('manifest')
        manifest = []
        for weapon in manifest_data:
            manifest.append(Weapon.from_json(weapon))
        return Smithy(manifest=manifest, coins=json_data.get('coins'))
