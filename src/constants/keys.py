from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from constants.enums import KeyMod, Location, MenuKeys, ShipConfig, PortVisit


MODIFIERS = {
    1: KeyMod.SHIFT,
    2: KeyMod.SHIFT,
    256: KeyMod.OPTION,
    512: KeyMod.OPTION,
    1024: KeyMod.COMMAND,
    2048: KeyMod.COMMAND,
}

MENU_KEYS = {
    K_UP: MenuKeys.UP,
    K_RIGHT: MenuKeys.RIGHT,
    K_LEFT: MenuKeys.LEFT,
    K_DOWN: MenuKeys.DOWN,
}

SHIP_KEYS = {
    K_UP: ShipConfig.SAILS,
    K_RIGHT: ShipConfig.CARGO,
    K_LEFT: ShipConfig.CREW,
    K_DOWN: ShipConfig.WEAPONS,
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
    K_UP: PortVisit.SHIPYARD,  # ship upgrades (crew capacity, cargo weight/volume, sails
    K_RIGHT: PortVisit.MERCHANT,  # buy/sell cargo
    K_LEFT: PortVisit.TAVERN,  # hire/release crew
    K_DOWN: PortVisit.SMITHY,  # buy/sell weapons
}

REPAIR_KEYS = {
    K_UP: "sails",
    K_RIGHT: "shipyard",
    K_LEFT: "crew",  # TODO: remove this once "hire crew" implemented in port_keys - this becomes tavern (for rumors)
    K_DOWN: "engineer",
}
