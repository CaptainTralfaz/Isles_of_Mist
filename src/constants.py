from pygame import image, font

from enums import ItemType
from tile import Elevation

font.init()

margin = 5
block_size = 4
tile_size = 32
map_width = 48
map_height = 48
caption = "Isles of Mist"

# TODO YAML
# images = {}
# with open(file="data/images.yaml", mode="r") as file:
#     data = yaml.safe_load(file)
#     for icon_type in data.keys():
#         for icon in icon_type:
#             images[icon] = image.load(f"assets/{icon_type}/{icon_type[icon]}]")
# print(images)
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

compass = image.load("assets/misc/compass.png")
pointer = image.load("assets/misc/pointer.png")
arrow_key = image.load("assets/misc/arrow_key.png")
cloud = image.load("assets/misc/cloud.png")
haze = image.load("assets/misc/haze.png")
moon = image.load("assets/misc/moon.png")
moon_shadow = image.load("assets/misc/moon_shadow.png")
rain = image.load("assets/misc/rain.png")
sky = image.load("assets/misc/sky.png")
storm = image.load("assets/misc/storm.png")
sun = image.load("assets/misc/sun.png")

player_image = image.load("assets/entities/ship_icon.png")
turtle_image = image.load("assets/entities/turtle.png")
serpent_image = image.load("assets/entities/serpent.png")
bat_image = image.load("assets/entities/bat.png")
carcass = image.load("assets/entities/carcass.png")
shipwreck = image.load("assets/entities/shipwreck.png")
chest = image.load("assets/entities/chest.png")
bottle = image.load("assets/entities/bottle.png")
mermaid_image = image.load("assets/entities/mermaid.png")

ocean = image.load("assets/terrain/ocean.png")
water = image.load("assets/terrain/water.png")
shallows = image.load("assets/terrain/shallows.png")
beach = image.load("assets/terrain/beach.png")
grass = image.load("assets/terrain/grass.png")
jungle = image.load("assets/terrain/jungle.png")
mountain = image.load("assets/terrain/mountain.png")
volcano = image.load("assets/terrain/volcano.png")
fog_of_war = image.load("assets/terrain/fog_of_war.png")
mist = image.load("assets/terrain/mist.png")
highlight = image.load("assets/terrain/highlight.png")
minefield = image.load("assets/terrain/minefield.png")

port = image.load("assets/terrain/port.png")
coral = image.load("assets/terrain/coral.png")
rocks = image.load("assets/terrain/rocks.png")
sandbar = image.load("assets/terrain/sandbar.png")
seaweed = image.load("assets/terrain/seaweed.png")

mast_0 = image.load("assets/entities/mast_0.png")
mast_1 = image.load("assets/entities/mast_1.png")
mast_2 = image.load("assets/entities/mast_2.png")
mast_3 = image.load("assets/entities/mast_3.png")
mast_4 = image.load("assets/entities/mast_4.png")

images = {
    'mast_0': mast_0,
    'mast_1': mast_1,
    'mast_2': mast_2,
    'mast_3': mast_3,
    'mast_4': mast_4,
    'turtle_image': turtle_image,
    'serpent_image': serpent_image,
    'bat_image': bat_image,
    'mermaid_image': mermaid_image,
    'carcass': carcass,
    'shipwreck': shipwreck,
    'chest': chest,
    'bottle': bottle,
    'ocean': ocean,
    'water': water,
    'shallows': shallows,
    'beach': beach,
    'grass': grass,
    'jungle': jungle,
    'mountain': mountain,
    'volcano': volcano,
    'fog_of_war': fog_of_war,
    'mist': mist,
    'coral': coral,
    'rocks': rocks,
    'sandbar': sandbar,
    'seaweed': seaweed,
    'port': port,
    'highlight': highlight,
    'minefield': minefield,
    'arrow_key': arrow_key,
    'compass': compass,
    'pointer': pointer,
    'cloudy': cloud,
    'hazy': haze,
    'sun': sun,
    'moon': moon,
    'moon_shadow': moon_shadow,
    'rainy': rain,
    'clear': sky,
    'stormy': storm,
}

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

arrows = image.load("assets/cargo/arrows.png")
bat_wing = image.load("assets/cargo/bat wing.png")
bolts = image.load("assets/cargo/bolts.png")
bread = image.load("assets/cargo/bread.png")
brick = image.load("assets/cargo/brick.png")
cannonballs = image.load("assets/cargo/cannonballs.png")
canvas = image.load("assets/cargo/canvas.png")
fish = image.load("assets/cargo/fish.png")
fruit = image.load("assets/cargo/fruit.png")
grain = image.load("assets/cargo/grain.png")
leather = image.load("assets/cargo/leather.png")
log = image.load("assets/cargo/log.png")
map_image = image.load("assets/cargo/map.png")
meat = image.load("assets/cargo/meat.png")
message = image.load("assets/cargo/message.png")
mines = image.load("assets/cargo/mines.png")
pearl = image.load("assets/cargo/pearl.png")
rope = image.load("assets/cargo/rope.png")
rum = image.load("assets/cargo/rum.png")
salt = image.load("assets/cargo/salt.png")
scale = image.load("assets/cargo/scale.png")
shell = image.load("assets/cargo/shell.png")
skins = image.load("assets/cargo/skins.png")
stone = image.load("assets/cargo/stone.png")
tar = image.load("assets/cargo/tar.png")
water = image.load("assets/cargo/water.png")
wood = image.load("assets/cargo/wood.png")

cargo_icons = {
    'arrows': arrows,
    'bat wing': bat_wing,
    'bolts': bolts,
    'bread': bread,
    'brick': brick,
    'cannonballs': cannonballs,
    'canvas': canvas,
    'fish': fish,
    'fruit': fruit,
    'grain': grain,
    'leather': leather,
    'log': log,
    'map': map_image,
    'meat': meat,
    'message': message,
    'mines': mines,
    'pearl': pearl,
    'rope': rope,
    'rum': rum,
    'salt': rum,
    'scale': scale,
    'shell': shell,
    'skins': skins,
    'stone': stone,
    'tar': tar,
    'water': water,
    'wood': wood,
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
    'fly': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS, Elevation.BEACH, Elevation.GRASS, Elevation.JUNGLE],
    'shore': [Elevation.SHALLOWS, Elevation.BEACH],
    'shallows': [Elevation.SHALLOWS],
    'all': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS,
            Elevation.BEACH, Elevation.GRASS, Elevation.JUNGLE, Elevation.MOUNTAIN, Elevation.VOLCANO]
}

item_stats = {
    'canvas': {
        'weight': 2,
        'volume': 4,
        'category': ItemType.GOODS,
    },
    'rope': {
        'weight': 1,
        'volume': 1,
        'category': ItemType.GOODS,
    },
    'tar': {
        'weight': 3,
        'volume': 3,
        'category': ItemType.GOODS,
    },
    'wood': {
        'weight': 2,
        'volume': 4,
        'category': ItemType.GOODS,
    },
    'meat': {
        'weight': 1,
        'volume': 1,
        'category': ItemType.SUPPLIES,
    },
    'rum': {
        'weight': 1,
        'volume': 1,
        'category': ItemType.SUPPLIES,
    },
    'fish': {
        'weight': 1,
        'volume': 1,
        'category': ItemType.SUPPLIES,
    },
    'fruit': {
        'weight': 1,
        'volume': 1,
        'category': ItemType.SUPPLIES,
    },
    'water': {
        'weight': 2,
        'volume': 3,
        'category': ItemType.SUPPLIES,
    },
    'pearl': {
        'weight': 0,
        'volume': 0,
        'category': ItemType.MONEY,
    },
    'bat wing': {
        'weight': 1,
        'volume': 3,
        'category': ItemType.EXOTICS,
    },
    
    'map': {
        'weight': 1,
        'volume': 1,
        'category': ItemType.EXOTICS,
    },
    'message': {
        'weight': 0,
        'volume': 0,
        'category': ItemType.EXOTICS,
    },
    'shell': {
        'weight': 5,
        'volume': 5,
        'category': ItemType.EXOTICS,
    },
    'scale': {
        'weight': 2,
        'volume': 3,
        'category': ItemType.EXOTICS,
    },
    'arrows': {
        'weight': .1,
        'volume': .1,
        'category': ItemType.AMMO,
    },
    'bolts': {
        'weight': 1,
        'volume': 2,
        'category': ItemType.AMMO,
    },
    'cannonballs': {
        'weight': 2,
        'volume': 1,
        'category': ItemType.AMMO,
    },
    'mines': {
        'weight': 2,
        'volume': 2,
        'category': ItemType.AMMO,
    },
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
