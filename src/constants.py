from pygame import image, font

from tile import Elevation

font.init()

margin = 5
block_size = 4
tile_size = 32
map_width = 48
map_height = 48
caption = "Isles of Mist"

# TODO Variable later ??
game_font = font.Font('freesansbold.ttf', 16)
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
arrows = image.load("assets/misc/arrows.png")
bolts = image.load("assets/misc/bolts.png")
cannonballs = image.load("assets/misc/cannonballs.png")
mines = image.load("assets/misc/mines.png")

player_image = image.load("assets/entities/ship_icon.png")
turtle_image = image.load("assets/entities/turtle.png")
serpent_image = image.load("assets/entities/serpent.png")
bat_image = image.load("assets/entities/bat.png")
carcass = image.load("assets/entities/carcass.png")
shipwreck = image.load("assets/entities/shipwreck.png")
chest = image.load("assets/entities/chest.png")
bottle = image.load("assets/entities/bottle.png")
mermaid_image = image.load("assets/entities/mermaid.png")

sprite_sheet = image.load("assets/entities/sprite_sheet.png")

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
    'mines': mines,
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
    'arrows': arrows,
    'bolts': bolts,
    'cannonballs': cannonballs,
}

colors = {
    'white': (255, 255, 255),
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
        'category': 'goods',
    },
    'rope': {
        'weight': 1,
        'volume': 1,
        'category': 'goods',
    },
    'tar': {
        'weight': 3,
        'volume': 3,
        'category': 'goods',
    },
    'wood': {
        'weight': 2,
        'volume': 4,
        'category': 'goods',
    },
    'meat': {
        'weight': 1,
        'volume': 1,
        'category': 'supplies',
    },
    'rum': {
        'weight': 1,
        'volume': 1,
        'category': 'supplies',
    },
    'fish': {
        'weight': 1,
        'volume': 1,
        'category': 'supplies',
    },
    'fruit': {
        'weight': 1,
        'volume': 1,
        'category': 'supplies',
    },
    'water': {
        'weight': 2,
        'volume': 3,
        'category': 'supplies',
    },
    'pearl': {
        'weight': 0,
        'volume': 0,
        'category': 'exotics',
    },
    'map': {
        'weight': 1,
        'volume': 1,
        'category': 'exotics',
    },
    'message': {
        'weight': 0,
        'volume': 0,
        'category': 'exotics',
    },
    'shell': {
        'weight': 5,
        'volume': 5,
        'category': 'exotics',
    },
    'scale': {
        'weight': 2,
        'volume': 3,
        'category': 'exotics',
    },
    'bat wing': {
        'weight': 1,
        'volume': 3,
        'category': 'exotics',
    },
    'cannonballs': {
        'weight': 2,
        'volume': 1,
        'category': 'ammo',
    },
    'bolts': {
        'weight': 1,
        'volume': 2,
        'category': 'ammo',
    },
    'mines': {
        'weight': 2,
        'volume': 2,
        'category': 'ammo',
    },
    'arrows': {
        'weight': .1,
        'volume': .1,
        'category': 'ammo',
    },
    'ballista': {
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
