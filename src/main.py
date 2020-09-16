#!/usr/bin/env python3
import copy

import pygame

import entity_factory
from colors import colors
from engine import Engine
from procgen import generate_map
from tile import tile_size


def main() -> None:
    pygame.init()
    fps_clock = pygame.time.Clock()
    
    caption = "Isles of Mist"
    icon = pygame.image.load("assets/ship_icon.png")
    
    map_width = 24
    map_height = 24
    screen_width = 20 * tile_size - 10 + 200
    screen_height = 20 * tile_size - 16 + 200
    
    game_display = pygame.display.set_mode((screen_width, screen_height))
    game_display.fill(colors["black"])
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    pygame.display.flip()
    
    should_quit = False
    
    player = copy.deepcopy(entity_factory.player)
    
    engine = Engine(player=player)
    
    engine.game_map = generate_map(map_width, map_height, engine=engine)
    
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", colors["welcome_text"]
    )
    while not should_quit:
        try:
            engine.event_handler.handle_events()
        
        except SystemExit:
            should_quit = True
        
        engine.render(main_surface=game_display)
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()
