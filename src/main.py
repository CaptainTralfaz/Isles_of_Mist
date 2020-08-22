#!/usr/bin/env python3
import pygame

from pygame import Surface
from src.input_handlers import MainEventHandler
from src.actions import ActionQuit, RotateAction, MovementAction
from src.render_functions import rot_center
from src.utilities import direction_angle, move_entity


def main() -> None:
    pygame.init()
    fps_clock = pygame.time.Clock()
    
    caption = "Isles of Mist"
    icon = pygame.image.load("assets/Ship_s.png")
    player_image = pygame.image.load("assets/Ship_s.png")
    player_facing = 0
    
    screen_width = 800
    screen_height = 500
    tilesize = 32
    
    player_x = 12 * tilesize
    player_y = 6 * tilesize
    
    main_surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    should_quit = False

    event_handler = MainEventHandler()

    while not should_quit:
        try:
            main_surface.blit(player_image, (player_x, player_y + ((player_x // tilesize) % 2) * tilesize // 2))
            pygame.display.flip()
            
            action = event_handler.handle_events(player_facing)
            
            if action is None:
                continue
                
            if isinstance(action, RotateAction):
                player_facing += action.rotate
                if player_facing >= len(direction_angle):
                    player_facing = 0
                elif player_facing < 0:
                    player_facing = len(direction_angle) - 1
                print(player_facing)
            
            elif isinstance(action, MovementAction):
                player_x, player_y = move_entity(player_x, player_y, action.direction)
                
            elif isinstance(action, ActionQuit):
                raise SystemExit()
            
            print(player_x, player_y)
            main_surface.fill((0, 0, 0))
            player_image = rot_center(icon, direction_angle[player_facing])
            
        except SystemExit:
            should_quit = True

    pygame.quit()


if __name__ == "__main__":
    main()
