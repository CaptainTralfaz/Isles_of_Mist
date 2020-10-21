from components.broadsides import Broadsides
from components.cargo import Cargo
from components.crew import Crew
from components.fighter import Fighter
from components.sails import Sails
from components.view import View
from components.weapon import Weapon
from constants.sprites import animation_speed, flicker_timer, sprite_count
from entity import Entity
from sprite import Sprite

player = Entity(x=0,
                y=0,
                facing=0,
                elevations='water',
                icon='mast_1',
                name='Player',
                ai_cls_name='NeutralEnemy',
                fighter=Fighter(hp=15,
                                defense=1,
                                power=5,
                                name="hull",
                                can_hit={"body": 100}),
                sails=Sails(hp=10,
                            defense=0,
                            raised=False,
                            name="sail"),
                crew=Crew(max_count=10,
                          defense=0,
                          name="crew"),
                broadsides=Broadsides(slot_count=1,
                                      port=[Weapon.make_weapon_from_name('ballista')],
                                      starboard=[Weapon.make_weapon_from_name('ballista')],
                                      storage=[]),
                cargo=Cargo(max_weight=1000,
                            max_volume=1000,
                            coins=100,
                            manifest={
                                'rope': 10,
                                'wood': 10,
                                'meat': 10,
                                'water': 10,
                                'tar': 10,
                                'canvas': 10,
                                'bolts': 20,
                                'arrows': 100,
                            }),
                view=View(5))

turtle = Entity(x=0,
                y=0,
                facing=0,
                elevations='water',
                icon='turtle_image',
                sprite=Sprite(sprite_name="turtle_sprite",
                              sprite_count=sprite_count,
                              flicker_timer=flicker_timer,
                              animation_speed=animation_speed),
                name='Turtle',
                ai_cls_name='NeutralEnemy',
                fighter=Fighter(hp=10,
                                defense=4,
                                power=3,
                                can_hit={}),
                view=View(1))

serpent = Entity(x=0,
                 y=0,
                 facing=0,
                 elevations='deep_water',
                 icon='serpent_image',
                 name='Serpent',
                 sprite=Sprite(sprite_name="serpent_sprite",
                               sprite_count=sprite_count,
                               flicker_timer=flicker_timer,
                               animation_speed=animation_speed * 2),
                 ai_cls_name='HostileEnemy',
                 fighter=Fighter(hp=6,
                                 defense=1,
                                 power=3,
                                 can_hit={"hull": 60, "crew": 5, "weapon": 15}),
                 view=View(4))

bat = Entity(x=0,
             y=0,
             facing=0,
             elevations='fly',
             icon='bat_image',
             name='Bat',
             sprite=Sprite(sprite_name="bat_sprite",
                           sprite_count=sprite_count,
                           flicker_timer=flicker_timer,
                           animation_speed=animation_speed / 2),
             ai_cls_name='HostileFlyingEnemy',
             fighter=Fighter(hp=3,
                             defense=0,
                             power=2,
                             can_hit={"sail": 30, "crew": 10}),
             view=View(5),
             flying=True)

mermaid = Entity(x=0,
                 y=0,
                 facing=0,
                 elevations='shore',
                 icon='mermaid_image',
                 name='Mermaid',
                 sprite=Sprite(sprite_name="mermaid_sprite",
                               sprite_count=sprite_count,
                               flicker_timer=flicker_timer,
                               animation_speed=animation_speed / 1),
                 ai_cls_name='HostileEnemy',
                 fighter=Fighter(hp=2,
                                 defense=0,
                                 power=1,
                                 can_hit={"crew": 10}),
                 view=View(4))

shipwreck = Entity(x=0,
                   y=0,
                   elevations='shallows',
                   icon='shipwreck',
                   name='Shipwreck')

bottle = Entity(x=0,
                y=0,
                elevations='water',
                icon='bottle',
                name='Bottle')

chest = Entity(x=0,
               y=0,
               elevations='ocean',
               icon='chest',
               name='Chest')
