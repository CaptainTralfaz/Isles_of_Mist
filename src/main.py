#!/usr/bin/env python3

import pygame

from constants.colors import colors
from constants.constants import map_width, map_height, caption
from constants.images import misc_icons
from game import Game
from game import new_game, load_game
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
    
    should_quit = False
    while not should_quit:
        game_display.fill(colors['black'])
        main_menu_render(main_display=game_display, ui_layout=ui_layout)
        pygame.display.flip()
        # noinspection PyArgumentList
        events = pygame.event.get(pump=True)
        for event in events:
            if event.type == pygame.QUIT:
                should_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP]:
                    player, engine = new_game(ui_layout=ui_layout)
                    Game(game_display, engine).play_game()
                elif event.key in [pygame.K_DOWN]:
                    # load game
                    player, engine = load_game(ui_layout=ui_layout)
                    Game(game_display, engine).play_game()
                elif event.key == pygame.K_ESCAPE:
                    should_quit = True
    
    pygame.quit()


if __name__ == "__main__":
    main()
