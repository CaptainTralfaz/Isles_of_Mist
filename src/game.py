import copy
import random
from json import dump, load

from pygame import display

import entity_factory
from constants.colors import colors
from constants.constants import map_width, map_height, FPS
from engine import Engine
from procgen import generate_map


class Game:
    def __init__(self, main_surface, engine):
        self.display = main_surface
        self.engine = engine
    
    def play_game(self):
        should_quit = False
        
        while not should_quit:
            try:
                something_happened = self.engine.event_handler.handle_events()
                if something_happened:
                    save_game(self.engine, self.engine.game_map, self.engine.player)
            except SystemExit:
                should_quit = True
            
            self.engine.render_all(main_surface=self.display)
            display.flip()
            self.engine.clock.tick(FPS)
        

def new_game(ui_layout):
    seed = random.randint(0, 10000)  # 8617
    print(seed)
    random.seed(seed)
    
    player = copy.deepcopy(entity_factory.player)
    
    engine = Engine(player=player, ui_layout=ui_layout)
    engine.game_map = generate_map(map_width, map_height, engine=engine, seed=seed, ui_layout=ui_layout)
    
    engine.message_log.add_message(
        "Hello and welcome, Captain, to the Isles of Mist", colors['aqua']
    )
    
    return player, engine


def load_game(ui_layout):
    seed = random.randint(0, 10000)  # 8617
    print(seed)
    random.seed(seed)
    
    player = copy.deepcopy(entity_factory.player)
    
    engine = Engine(player=player, ui_layout=ui_layout)
    engine.game_map = generate_map(map_width, map_height, engine=engine, seed=seed, ui_layout=ui_layout)
    
    engine.message_log.add_message(
        "Welcome back, Captain, to the Isles of Mist", colors['aqua']
    )
    
    return player, engine


def save_game(engine, game_map, player):
    data = {
        'engine': engine.to_json()
    }
    with open('data/saved_engine.json', 'w') as save_file:
        dump(data, save_file, indent=4)
        
    data = {
        'game_map': game_map.to_json()
    }
    with open('data/saved_game_map.json', 'w') as save_file:
        dump(data, save_file, indent=4)

    data = {
        'player': player.to_json()
    }
    with open('data/saved_player.json', 'w') as save_file:
        dump(data, save_file, indent=4)
