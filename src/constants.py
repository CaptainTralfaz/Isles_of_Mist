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
view_port = 9
message_count = 10

time_tick = 2
FPS = 20
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
mines = image.load("assets/terrain/mines.png")

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
    'mines': (200, 0, 0),
    'port': (255, 255, 255),
}

move_elevations = {
    'water': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS],
    'land': [Elevation.BEACH, Elevation.GRASS, Elevation.JUNGLE, Elevation.MOUNTAIN, Elevation.VOLCANO],
    'fly': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS, Elevation.BEACH, Elevation.GRASS, Elevation.JUNGLE],
    'shore': [Elevation.SHALLOWS, Elevation.BEACH],
    'shallows': [Elevation.SHALLOWS],
    'all': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS,
            Elevation.BEACH, Elevation.GRASS, Elevation.JUNGLE, Elevation.MOUNTAIN, Elevation.VOLCANO]
}

# TODO add weight / volume of weapons
weapons = {
    'ballista': {'hp': 3,
                 'defense': 2,
                 'range': 3,
                 'power': 3,
                 'cooldown': 4},
    'heavy ballista': {'hp': 4,
                       'defense': 2,
                       'range': 4,
                       'power': 4,
                       'cooldown': 4},
    'repeating ballista': {'hp': 3,
                           'defense': 2,
                           'range': 3,
                           'power': 3,
                           'cooldown': 3},
    'cannon': {'hp': 5,
               'defense': 3,
               'range': 4,
               'power': 5,
               'cooldown': 5},
    'organ gun': {'hp': 5,
                  'defense': 3,
                  'range': 4,
                  'power': 4,
                  'cooldown': 4},
    'heavy cannon': {'hp': 6,
                     'defense': 4,
                     'range': 5,
                     'power': 6,
                     'cooldown': 6},
    'longguns': {'hp': 5,
                 'defense': 4,
                 'range': 6,
                 'power': 5,
                 'cooldown': 6},
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
}
