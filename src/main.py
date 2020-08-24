#!/usr/bin/env python3
import pygame

from src.engine import Engine
from src.entity import Entity
from src.input_handlers import MainEventHandler
from src.procgen import generate_map


def main() -> None:
    pygame.init()
    fps_clock = pygame.time.Clock()
    
    caption = "Isles of Mist"
    icon = pygame.image.load("assets/Ship_s.png")
    player_image = pygame.image.load("assets/Ship_s.png")
    
    tile_size = 32
    map_width = 30
    map_height = 20
    screen_width = map_width * tile_size
    screen_height = map_height * tile_size
    
    game_display = pygame.display.set_mode((screen_width, screen_height))
    game_display.fill((0, 0, 175))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    pygame.display.flip()
    
    should_quit = False
    
    event_handler = MainEventHandler()
    
    player = Entity(x=12 * tile_size, y=6 * tile_size, facing=0, icon=player_image
                    )
    npc = Entity(x=6 * tile_size, y=6 * tile_size, facing=0, icon=icon)
    entities = {player, npc}
    
    game_map = generate_map(map_width, map_height)
    
    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)
    
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
