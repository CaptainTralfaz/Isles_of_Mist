from pygame import image, font

font.init()

margin = 5
block_size = 4
tile_size = 32
map_width = 48
map_height = 48
caption = "Isles of Mist"

# TODO Variable later ??
game_font = font.Font('freesansbold.ttf', 16)
view_port = 7
message_count = 10

FPS = 20
sprite_count = 4
animation_speed = 2.0
flicker_timer = 0.0
sprite_image = 0

icon = image.load("assets/misc/compass.png")
arrow_key = image.load("assets/misc/arrow_key.png")

player_image = image.load("assets/entities/ship_icon.png")
turtle_image = image.load("assets/entities/turtle.png")
serpent_image = image.load("assets/entities/serpent.png")
bat_image = image.load("assets/entities/bat.png")
carcass = image.load("assets/entities/carcass.png")
sunken_ship = image.load("assets/entities/sunken_ship.png")

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

bat_sprite = []
serpent_sprite = []
turtle_sprite = []
for i in range(sprite_count):
    bat_sprite.append(sprite_sheet.subsurface(i * tile_size, tile_size * 0, tile_size, tile_size))
    serpent_sprite.append(sprite_sheet.subsurface(i * tile_size, tile_size * 1, tile_size, tile_size))
    turtle_sprite.append(sprite_sheet.subsurface(i * tile_size, tile_size * 2, tile_size, tile_size))
sprites = {
    'turtle_sprite': turtle_sprite,
    'serpent_sprite': serpent_sprite,
    'bat_sprite': bat_sprite,
}

images = {
    'player_image': player_image,
    'turtle_image': turtle_image,
    'serpent_image': serpent_image,
    'bat_image': bat_image,
    'carcass': carcass,
    'sunken_ship': sunken_ship,
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
    'highlight': highlight,
    'mines': mines,
    'arrow_key': arrow_key,
}

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "player_atk": (225, 225, 225),
    "enemy_atk": (255, 200, 200),
    "player_die": (255, 50, 50),
    "enemy_die": (255, 150, 50),
    "welcome_text": (25, 150, 255),
    "bar_text": (255, 255, 255),
    "bar_filled": (0, 100, 0),
    "bar_empty": (75, 25, 25),
    "invalid": (255, 255, 0),
    "impossible": (125, 125, 125),
    "error": (255, 75, 75),
    "health_recovered": (0, 255, 0),
    'ocean': (0, 0, 175),
    'water': (0, 50, 200),
    'shallows': (0, 75, 225),
    'beach': (225, 200, 125),
    'grass': (50, 175, 50),
    'jungle': (0, 125, 0),
    'mountain': (225, 225, 225),
    'volcano': (200, 0, 0),
    'coral': (255, 115, 200),
    'rocks': (225, 225, 225),
    'seaweed': (50, 175, 50),
    'sandbar': (225, 200, 125),
    'mines': (200, 0, 0),
}
