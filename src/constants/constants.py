from pygame import font

from constants.enums import Elevation

font.init()

margin = 5
block_size = 4
tile_size = 32
map_width = 48
map_height = 48
caption = "Isles of Mist"

view_port = 9
message_count = 10

time_tick = 2
FPS = 30

wind_min_count = 25
conditions_min_count = 50

# TODO Variable later ??
# game_font = font.Font('freesansbold.ttf', 16)  # Original
# game_font = font.SysFont('chalkboardttc', 14)
game_font = font.SysFont('georgiabolditalicttf', 14)  # VERY nice
# game_font = font.SysFont('verdanabolditalicttf', 12)  # BEST

move_elevations = {
    'water': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS],
    'deep_water': [Elevation.OCEAN, Elevation.WATER],
    'ocean': [Elevation.OCEAN],
    'land': [Elevation.BEACH, Elevation.GRASS, Elevation.JUNGLE, Elevation.MOUNTAIN, Elevation.VOLCANO],
    'fly': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS,
            Elevation.BEACH, Elevation.GRASS, Elevation.JUNGLE],
    'shore': [Elevation.SHALLOWS, Elevation.BEACH],
    'shallows': [Elevation.SHALLOWS],
    'all': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS, Elevation.BEACH,
            Elevation.GRASS, Elevation.JUNGLE, Elevation.MOUNTAIN, Elevation.VOLCANO]
}

SMITHY = {
    'ballista': 100,
    'heavy ballista': 20,
    'repeating ballista': 20,
    'sniper ballista': 20,
    'cannon': 10,
    'organ gun': 5,
    'heavy cannon': 5,
    'long guns': 5,
}

MERCHANT = {
    'bread': 20,
    'brick': 25,
    'canvas': 20,
    'fish': 30,
    'fruit': 10,
    'grain': 30,
    'leather': 10,
    'lumber': 30,
    'meat': 30,
    'rope': 20,
    'rum': 10,
    'salt': 10,
    'skins': 30,
    'stone': 30,
    'tar': 10,
    'water': 30,
    'wood': 30,
    'arrows': 20,
    'bolts': 20,
    'cannonballs': 10,
    'mines': 10,
}
