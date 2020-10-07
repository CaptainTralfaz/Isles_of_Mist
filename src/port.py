from typing import Dict, Tuple
from random import choice, randint


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
        

def gen_port_name() -> str:
    first = randint(0, 1)
    if first == 1:
        prefix = choice(["Port ", "Cape ", "St. ", "Grand ", "Little ", "Poor"])
    else:
        prefix = ""
    name = choice(["Parrot", "Sugar", "Rum", "Sand", "Coral", "Booty", "Doom", "Happy", "Drunken", "Voodoo", "Pirate"])
    if first == 1:
        second = randint(0, 1)
    else:
        second = 1
    if first == 0 or second == 1:
        postfix = choice([" Harbor", " Hook", " Bay", " Town", "ville", "town"])
    else:
        postfix = ""
    return f"{prefix}{name}{postfix}"


def gen_merchant() -> Dict[str, int]:
    merchant = {}
    return merchant


def gen_smithy() -> Dict[str, int]:
    smithy = {}
    return smithy
