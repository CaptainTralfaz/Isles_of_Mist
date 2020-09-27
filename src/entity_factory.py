from components.ai import NeutralEnemy, HostileEnemy
from components.broadsides import Broadsides
from components.cargo import Cargo
from components.crew import Crew
from components.fighter import Fighter
from components.sails import Sails
from components.view import View
from constants import animation_speed, flicker_timer, sprite_count, move_elevations
from entity import Actor, Entity
from sprite import Sprite

player = Actor(x=0,
               y=0,
               facing=0,
               elevations=move_elevations['water'],
               icon='mast_1',
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
               crew=Crew(count=10,
                         max_count=10,
                         defense=1,
                         name="crew"),
               broadsides=Broadsides(slot_count=1, port=['heavy cannon'], starboard=['heavy cannon']),
               cargo=Cargo(max_weight=200,
                           max_volume=200,
                           manifest={'rope': 10,
                                     'wood': 10,
                                     'meat': 10,
                                     'water': 10,
                                     'tar': 10,
                                     'canvas': 10,
                                     }),
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
                fighter=Fighter(hp=7,
                                defense=2,
                                power=4,
                                can_hit={"hull": 60, "crew": 10, "weapon": 10}),
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
            fighter=Fighter(hp=4,
                            defense=1,
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
                sprite=Sprite(sprite_name="mermaid_sprite",
                              sprite_count=sprite_count,
                              flicker_timer=flicker_timer,
                              animation_speed=animation_speed / 1),
                ai_cls=HostileEnemy,
                fighter=Fighter(hp=3,
                                defense=0,
                                power=2,
                                can_hit={"crew": 10}),
                view=View(4))

shipwreck = Entity(x=0,
                   y=0,
                   elevations=move_elevations['shallows'],
                   icon='shipwreck',
                   name='Shipwreck',
                   )

bottle = Entity(x=0,
                y=0,
                elevations=move_elevations['water'],
                icon='bottle',
                name='Bottle',
                )

chest = Entity(x=0,
               y=0,
               elevations=move_elevations['water'],
               icon='chest',
               name='Chest',
               )
