#!/usr/bin/env python3
import pygame
import copy
import src.entity_factory

from src.engine import Engine
from src.entity import Entity
from src.input_handlers import MainEventHandler
from src.procgen import generate_map


def main() -> None:
    pygame.init()
    fps_clock = pygame.time.Clock()
    
    caption = "Isles of Mist"
    icon = pygame.image.load("assets/ship_icon.png")

    tile_size = 32
    map_width = 30
    map_height = 20
    screen_width = map_width * tile_size - 10
    screen_height = map_height * tile_size - 16
    
    game_display = pygame.display.set_mode((screen_width, screen_height))
    game_display.fill((0, 0, 175))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    pygame.display.flip()
    
    should_quit = False
    
    event_handler = MainEventHandler()

    player = copy.deepcopy(src.entity_factory.player)
    
    game_map = generate_map(map_width, map_height, entities={player})
    
    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)
    
    while not should_quit:
        try:
            engine.render(main_surface=game_display)
            pygame.display.flip()
            
            events = pygame.event.get(pump=True)
            
            engine.handle_events(events=events)
        
        except SystemExit:
            should_quit = True
    
    pygame.quit()


if __name__ == "__main__":
    main()
