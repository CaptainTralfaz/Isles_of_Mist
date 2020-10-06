#!/usr/bin/env python3
import copy
import random

import pygame

import entity_factory
from constants import colors, map_width, map_height, caption, misc_icons, FPS
from engine import Engine
from procgen import generate_map
from ui import DisplayInfo


def main() -> None:
    seed = random.randint(0, 10000)  # 8617
    print(seed)
    
    random.seed(seed)
    pygame.init()
    fps_clock = pygame.time.Clock()
    
    player = copy.deepcopy(entity_factory.player)
    ui_layout = DisplayInfo(map_width, map_height)
    
    engine = Engine(player=player, ui_layout=ui_layout)
    engine.game_map = generate_map(map_width, map_height, engine=engine, seed=seed)
    
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to the Isles of Mist", colors['aqua']
    )
    
    game_display = pygame.display.set_mode((ui_layout.display_width, ui_layout.display_height),
                                           flags=pygame.SCALED | pygame.RESIZABLE)
    game_display.fill(colors['black'])
    pygame.display.set_caption(caption)
    pygame.display.set_icon(misc_icons['compass'])
    pygame.display.flip()
    
    should_quit = False
    
    while not should_quit:
        try:
            engine.event_handler.handle_events()
        
        except SystemExit:
            should_quit = True
        
        engine.render_all(main_surface=game_display)
        pygame.display.flip()
        engine.clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()
