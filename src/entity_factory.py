from components.ai import NeutralEnemy, HostileEnemy
from components.crew import Crew
from components.fighter import Fighter
from components.sails import Sails
from components.view import View
from constants import animation_speed, flicker_timer, sprite_count
from entity import Actor
from sprite import Sprite
from tile import Elevation


move_elevations = {
    'water': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS],
    'fly': [Elevation.OCEAN, Elevation.WATER, Elevation.SHALLOWS, Elevation.BEACH, Elevation.GRASS, Elevation.JUNGLE],
    'shore': [Elevation.SHALLOWS, Elevation.BEACH],
}

player = Actor(x=0,
               y=0,
               facing=0,
               elevations=move_elevations['water'],
               icon='mast_2',
               name='Player',
               ai_cls=NeutralEnemy,
               fighter=Fighter(hp=20,
                               defense=2,
                               power=5,
                               name="hull",
                               can_hit={"body": 100}),
               sails=Sails(hp=10,
                           defense=1,
                           raised=False,
                           name="sail"),
               crew=Crew(count=15,
                         max_count=15,
                         defense=1,
                         name="crew"),
               view=View(5))

turtle = Actor(x=0,
               y=0,
               facing=0,
               elevations=move_elevations['water'],
               icon='turtle_image',
               sprite=Sprite(sprite_name="turtle_sprite",
                             sprite_count=sprite_count,
                             flicker_timer=flicker_timer,
                             animation_speed=animation_speed),
               name='Turtle',
               ai_cls=NeutralEnemy,
               fighter=Fighter(hp=10,
                               defense=4,
                               power=3,
                               can_hit={}),
               view=View(2))

serpent = Actor(x=0,
                y=0,
                facing=0,
                elevations=move_elevations['water'],
                icon='serpent_image',
                name='Serpent',
                sprite=Sprite(sprite_name="serpent_sprite",
                              sprite_count=sprite_count,
                              flicker_timer=flicker_timer,
                              animation_speed=animation_speed * 2),
                ai_cls=HostileEnemy,
                fighter=Fighter(hp=8,
                                defense=1,
                                power=4,
                                can_hit={"hull": 60, "crew": 10}),
                view=View(3))

bat = Actor(x=0,
            y=0,
            facing=0,
            elevations=move_elevations['fly'],
            icon='bat_image',
            name='Bat',
            sprite=Sprite(sprite_name="bat_sprite",
                          sprite_count=sprite_count,
                          flicker_timer=flicker_timer,
                          animation_speed=animation_speed / 2),
            ai_cls=HostileEnemy,
            fighter=Fighter(hp=5,
                            defense=0,
                            power=3,
                            can_hit={"sail": 30, "crew": 10}),
            view=View(4),
            flying=True)

mermaid = Actor(x=0,
            y=0,
            facing=0,
            elevations=move_elevations['shore'],
            icon='mermaid_image',
            name='Mermaid',
            ai_cls=HostileEnemy,
            fighter=Fighter(hp=4,
                            defense=1,
                            power=3,
                            can_hit={"crew": 10}),
            view=View(4))
