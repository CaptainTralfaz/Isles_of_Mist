#!/usr/bin/env python3
import copy

import pygame

import entity_factory
from colors import colors
from engine import Engine
from procgen import generate_map
from ui import DisplayInfo


def main() -> None:
    pygame.init()
    fps_clock = pygame.time.Clock()
    
    caption = "Isles of Mist"
    icon = pygame.image.load("assets/ship_icon.png")
    
    map_width = 48
    map_height = 48
    
    player = copy.deepcopy(entity_factory.player)
    ui_layout = DisplayInfo(map_width, map_height)
    
    engine = Engine(player=player, ui_layout=ui_layout)
    engine.game_map = generate_map(map_width, map_height, engine=engine)
    
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to the Isles of Mist", colors["welcome_text"]
    )
    
    game_display = pygame.display.set_mode((ui_layout.display_width, ui_layout.display_height))
    game_display.fill(colors["black"])
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    pygame.display.flip()
    
    should_quit = False
    
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
