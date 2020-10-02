from enum import Enum, auto


class GameStates(Enum):
    """
    Enum of possible game states
    """
    ACTION = auto()
    MAIN_MENU = auto()
    WEAPON_CONFIG = auto()
    CREW_CONFIG = auto()
    CARGO_CONFIG = auto()
    MERCHANT = auto()
    UPGRADES = auto()
    PLAYER_DEAD = auto()
