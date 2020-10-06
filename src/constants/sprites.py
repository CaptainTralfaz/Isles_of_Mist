from pygame import image
from constants.constants import tile_size


sprite_sheet = image.load("assets/entities/sprite_sheet.png")

sprite_count = 4
animation_speed = 2.0
flicker_timer = 0.0
sprite_image = 0

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
