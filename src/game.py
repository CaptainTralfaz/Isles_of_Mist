import copy
from json import dump, load

from pygame import display

import entity_factory
from constants.constants import map_width, map_height, FPS
from engine import Engine
from entity import Entity
from game_map import GameMap
from procgen import generate_map


class Game:
    def __init__(self, main_surface, engine, number):
        self.display = main_surface
        self.engine = engine
        self.number = number
    
    def play_game(self):
        should_quit = False
        
        while not should_quit:
            try:
                something_happened = self.engine.event_handler.handle_events()
                if something_happened:
                    save_game(self.engine, self.engine.game_map, self.engine.player, self.number)
            except SystemExit:
                should_quit = True
            
            self.engine.render_all(main_surface=self.display)
            display.flip()
            self.engine.clock.tick(FPS)


def new_game(ui_layout):
    player = copy.deepcopy(entity_factory.player)
    engine = Engine(player=player, ui_layout=ui_layout)
    engine.game_map = generate_map(map_width, map_height, engine=engine, seed=engine.seed, ui_layout=ui_layout)
    engine.message_log.add_message("Hello and welcome, Captain, to the Isles of Mist", text_color='aqua')
    
    return player, engine


def load_game(ui_layout, number):
    with open(f'data/save_game_{number}.json') as save_file:
        data = load(save_file)
        if data:
            player = Entity.from_json(data.get('player'))
            engine = Engine.from_json(player=player, json_data=data.get('engine'), ui_layout=ui_layout)
            engine.message_log.parent = engine
            engine.time.parent = engine
            game_map = GameMap.from_json(data.get('game_map'))
            game_map.weather.game_map = game_map
            game_map.engine = engine
            engine.game_map = game_map
            game_map.entities.add(player)
            for entity in game_map.entities:
                entity.parent = game_map
                if entity.view:
                    entity.view.set_fov()
        else:
            raise FileNotFoundError
    return player, engine


def save_game(engine, game_map, player, number):
    data = {
        'engine': engine.to_json(),
        'game_map': game_map.to_json(),
        'player': player.to_json()
    }
    with open(f'data/save_game_{number}.json', 'w') as save_file:
        dump(data, save_file, indent=4)
