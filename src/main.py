#!/usr/bin/env python3
from os import path
from typing import List

import pygame

from constants.colors import colors
from constants.constants import map_width, map_height, caption
from constants.images import misc_icons
from event_handlers.main_menu import MainMenuHandler
from render.main_menu import main_menu_render
from ui import DisplayInfo


def main() -> None:
    pygame.init()
    fps_clock = pygame.time.Clock()
    
    ui_layout = DisplayInfo(map_width, map_height)
    game_display = pygame.display.set_mode((ui_layout.display_width, ui_layout.display_height),
                                           flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption(caption)
    pygame.display.set_icon(misc_icons['compass'])
    
    shift_mod = False
    event_handler = MainMenuHandler(shift_mod=shift_mod)
    
    should_quit = False
    while not should_quit:
        available = available_loads()
        game_display.fill(colors['black'])
        main_menu_render(main_display=game_display, ui_layout=ui_layout,
                         shift_mod=event_handler.shift_mod, available_loads=available)
        pygame.display.flip()
        
        should_quit = event_handler.handle_events(game_display=game_display, ui_layout=ui_layout)
    
    pygame.quit()


def available_loads() -> List[int]:
    available = []
    for x in range(1, 5):
        if path.exists(f"data/saved_engine_{x}.json"):
            available.append(x)
    return available


if __name__ == "__main__":
    main()
