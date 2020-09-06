from pygame import image

from entity import Actor
from components.ai import NeutralEnemy, HostileEnemy
from components.fighter import Fighter
from components.view import View

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

player = Actor(x=0,
               y=0,
               facing=0,
               icon='player_image',
               name='Player',
               ai_cls=NeutralEnemy,
               fighter=Fighter(hp=10,
                               defense=2,
                               power=5),
               view=View(5))

turtle = Actor(x=0,
               y=0,
               facing=0,
               icon='turtle_image',
               name='Turtle',
               ai_cls=NeutralEnemy,
               fighter=Fighter(hp=10,
                               defense=2,
                               power=5),
               view=View(2))

serpent = Actor(x=0,
                y=0,
                facing=0,
                icon='serpent_image',
                name='Serpent',
                ai_cls=HostileEnemy,
                fighter=Fighter(hp=10,
                                defense=2,
                                power=5),
                view=View(3))

bat = Actor(x=0,
            y=0,
            facing=0,
            icon='bat_image',
            name='Bat',
            ai_cls=HostileEnemy,
            fighter=Fighter(hp=10,
                            defense=2,
                            power=5),
            view=View(4),
            flying=True)
