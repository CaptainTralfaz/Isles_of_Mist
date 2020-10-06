from pygame import image, font
from yaml import load, Loader

from enums import ItemType, Elevation

font.init()

margin = 5
block_size = 4
tile_size = 32
map_width = 48
map_height = 48
caption = "Isles of Mist"


def get_images():
    data = None
    with open(file="data/images.yaml", mode="r") as stream:
        try:
            data = load(stream, Loader=Loader)
        except FileNotFoundError:
            print(f"loading error on {stream}")
        entities = {}
        terrain = {}
        cargo = {}
        misc = {}
        image_dicts = {
            'entities': entities,
            'terrain': terrain,
            'cargo': cargo,
            'misc': misc,
        }
        for key in data['assets'].keys():
            for sprite in data['assets'][key]:
                # print(f"assets/{key}/{sprite}.png")
                icon = image.load(f"assets/{key}/{sprite}.png")
                image_dicts[key][sprite] = icon
        _entity_icons = image_dicts['entities']
        _terrain_icons = image_dicts['terrain']
        _cargo_icons = image_dicts['cargo']
        _misc_icons = image_dicts['misc']
    
    return _entity_icons, _terrain_icons, _cargo_icons, _misc_icons


entity_icons, terrain_icons, cargo_icons, misc_icons = get_images()


def get_items():
    data = None
    with open(file="data/items.yaml", mode="r") as stream:
        try:
            data = load(stream, Loader=Loader)
        except FileNotFoundError:
            print(f"loading error on {stream}")
        for item in data['item_stats'].keys():
            data['item_stats'][item]['category'] = ItemType(data['item_stats'][item]['category'])
        print(data['item_stats'])
    
    return data['item_stats']


item_stats = get_items()

# TODO Variable later ??
# game_font = font.Font('freesansbold.ttf', 16)  # Original
# game_font = font.SysFont('chalkboardttc', 14)
game_font = font.SysFont('georgiabolditalicttf', 14)  # VERY nice
# game_font = font.SysFont('verdanabolditalicttf', 12)  # BEST


view_port = 8
message_count = 10

time_tick = 2
FPS = 30
sprite_count = 4
animation_speed = 2.0
flicker_timer = 0.0
sprite_image = 0

sprite_sheet = image.load("assets/entities/sprite_sheet.png")

bat_sprite = []
serpent_sprite = []
turtle_sprite = []
mermaid_sprite = []
for i in range(sprite_count):
    bat_sprite.append(sprite_sheet.subsurface(i * tile_size, tile_size * 0, tile_size, tile_size))
    serpent_sprite.append(sprite_sheet.subsurface(i * tile_size, tile_size * 1, tile_size, tile_size))
    turtle_sprite.append(sprite_sheet.subsurface(i * tile_size, tile_size * 2, tile_size, tile_size))
    mermaid_sprite.append(sprite_sheet.subsurface(i * tile_size, tile_size * 3, tile_size, tile_size))

sprites = {
    'turtle_sprite': turtle_sprite,
    'serpent_sprite': serpent_sprite,
    'bat_sprite': bat_sprite,
    'mermaid_sprite': mermaid_sprite,
}

colors = {
    'white': (255, 255, 255),
    'lt_gray': (200, 200, 200),
    'dk_gray': (100, 100, 100),
    'dark': (25, 25, 25),
    'dark_green': (25, 50, 25),
    'black': (0, 0, 0),
    'pink': (225, 175, 175),
    'red': (250, 50, 50),
    'orange': (225, 150, 100),
    'bar_filled': (0, 100, 0),
    'bar_empty': (75, 25, 25),
    'invalid': (255, 255, 0),
    'gray': (125, 125, 125),
    'error': (255, 75, 75),
    'green': (0, 255, 0),
    'ocean': (0, 0, 175),
    'water': (0, 50, 200),
    'shallows': (0, 75, 225),
    'beach': (225, 200, 125),
    'grass': (50, 175, 50),
    'jungle': (0, 125, 0),
    'mountain': (225, 225, 225),
    'volcano': (200, 0, 0),
    'aqua': (0, 125, 255),
    'cyan': (0, 255, 255),
    'violet': (125, 0, 255),
    'purple': (255, 0, 255),
    'coral': (255, 115, 200),
    'rocks': (225, 225, 225),
    'seaweed': (50, 175, 50),
    'sandbar': (225, 200, 125),
    'minefield': (200, 0, 0),
}

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

weapon_stats = {'ballista': {
    'weight': 20,
    'volume': 25,
    'category': 'weapon',
},
    'heavy ballista': {
        'weight': 30,
        'volume': 30,
        'category': 'weapon',
    },
    'repeating ballista': {
        'weight': 25,
        'volume': 30,
        'category': 'weapon',
    },
    'sniper ballista': {
        'weight': 25,
        'volume': 35,
        'category': 'weapon',
    },
    'cannon': {
        'weight': 30,
        'volume': 20,
        'category': 'weapon',
    },
    'heavy cannon': {
        'weight': 40,
        'volume': 25,
        'category': 'weapon',
    },
    'organ gun': {
        'weight': 35,
        'volume': 25,
        'category': 'weapon',
    },
    'long guns': {
        'weight': 35,
        'volume': 30,
        'category': 'weapon',
    },
}

weapons = {
    'ballista': {'hp': 3,
                 'defense': 1,
                 'range': 3,
                 'power': 3,
                 'cooldown': 4,
                 'ammo': 'bolts',
                 },
    'heavy ballista': {'hp': 4,
                       'defense': 2,
                       'range': 3,
                       'power': 4,
                       'cooldown': 4,
                       'ammo': 'bolts',
                       },
    'repeating ballista': {'hp': 3,
                           'defense': 1,
                           'range': 3,
                           'power': 3,
                           'cooldown': 3,
                           'ammo': 'bolts',
                           },
    'sniper ballista': {'hp': 3,
                        'defense': 1,
                        'range': 4,
                        'power': 3,
                        'cooldown': 4,
                        'ammo': 'bolts',
                        },
    'cannon': {'hp': 5,
               'defense': 2,
               'range': 4,
               'power': 4,
               'cooldown': 5,
               'ammo': 'cannonballs',
               },
    'organ gun': {'hp': 4,
                  'defense': 2,
                  'range': 4,
                  'power': 4,
                  'cooldown': 4,
                  'ammo': 'cannonballs',
                  },
    'heavy cannon': {'hp': 6,
                     'defense': 3,
                     'range': 4,
                     'power': 6,
                     'cooldown': 6,
                     'ammo': 'cannonballs',
                     },
    'long guns': {'hp': 5,
                  'defense': 2,
                  'range': 5,
                  'power': 4,
                  'cooldown': 5,
                  'ammo': 'cannonballs',
                  },
}
