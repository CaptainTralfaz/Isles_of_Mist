from entity import Entity
from pygame import image

player_image = image.load("assets/ship_icon.png")
turtle_image = image.load("assets/turtle.png")
serpent_image = image.load("assets/serpent.png")
bat_image = image.load("assets/bat.png")

images = {
    'player_image': player_image,
    'turtle_image': turtle_image,
    'serpent_image': serpent_image,
    'bat_image': bat_image,
}


player = Entity(x=0, y=0, facing=0, icon='player_image')

turtle = Entity(x=0, y=0, facing=0, icon='turtle_image')

serpent = Entity(x=0, y=0, facing=0, icon='serpent_image')

bat = Entity(x=0, y=0, facing=0, icon='bat_image')
