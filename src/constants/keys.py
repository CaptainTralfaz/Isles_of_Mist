from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from constants.enums import KeyMod, Location


MODIFIERS = {
    1: KeyMod.SHIFT,
    2: KeyMod.SHIFT,
    256: KeyMod.OPTION,
    512: KeyMod.OPTION,
    1024: KeyMod.COMMAND,
    2048: KeyMod.COMMAND,
}

CONFIGURE_KEYS = {  # TODO: change arrow keys to enum??
    K_UP: "up",
    K_RIGHT: "right",
    K_LEFT: "left",
    K_DOWN: "down",
}

SHIP_KEYS = {
    K_UP: "sails",
    K_RIGHT: "cargo",
    K_LEFT: "crew",
    K_DOWN: "weapons",
}

ROTATE_KEYS = {
    K_LEFT: -1,
    K_RIGHT: 1
}

MOVEMENT_KEYS = {
    K_UP: 1
}

AUTO_KEYS = {
    K_DOWN
}

ATTACK_KEYS = {
    K_UP: Location.FORE,
    K_RIGHT: Location.STARBOARD,
    K_LEFT: Location.PORT,
    K_DOWN: Location.AFT,
}

PORT_KEYS = {
    K_UP: "shipyard",  # ship upgrades (crew capacity, cargo weight/volume, sails
    K_RIGHT: "merchant",  # buy/sell cargo
    K_LEFT: "barracks",  # hire/release crew
    K_DOWN: "tavern",  # buy/sell weapons
}

REPAIR_KEYS = {
    K_UP: "sails",
    K_RIGHT: "shipyard",
    K_LEFT: "crew",  # TODO: remove this once "hire crew" implemented in port_keys
    K_DOWN: "engineer",
}
