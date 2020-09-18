from components.ai import NeutralEnemy, HostileEnemy
from components.crew import Crew
from components.fighter import Fighter
from components.sails import Sails
from components.view import View
from entity import Actor

player = Actor(x=0,
               y=0,
               facing=0,
               icon='player_image',
               name='Player',
               ai_cls=NeutralEnemy,
               fighter=Fighter(hp=20,
                               defense=2,
                               power=5,
                               name="hull",
                               can_hit={"body": 100}),
               sails=Sails(hp=10,
                           defense=1,
                           raised=True,
                           name="sail"),
               crew=Crew(count=15,
                         max_count=15,
                         defense=0,
                         name="crew"),
               view=View(5))

turtle = Actor(x=0,
               y=0,
               facing=0,
               icon='turtle_image',
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
                icon='serpent_image',
                name='Serpent',
                ai_cls=HostileEnemy,
                fighter=Fighter(hp=8,
                                defense=1,
                                power=4,
                                can_hit={"hull": 60, "crew": 10}),
                view=View(3))

bat = Actor(x=0,
            y=0,
            facing=0,
            icon='bat_image',
            name='Bat',
            ai_cls=HostileEnemy,
            fighter=Fighter(hp=5,
                            defense=0,
                            power=3,
                            can_hit={"sail": 30, "crew": 10}),
            view=View(4),
            flying=True)
