#!/usr/bin/env python3
import pygame

from pygame import Surface
from src.input_handlers import MainEventHandler
from src.actions import ActionQuit, RotateAction, MovementAction
from src.render_functions import rot_center
from src.utilities import direction_angle
from src.entity import Entity


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

    player = Entity(x=12 * tilesize, y=6 * tilesize, facing=0, icon=player_image
                    )
    npc = Entity(x=6 * tilesize, y=6 * tilesize, facing=0, icon=player_image)
    entities = {player, npc}
    
    while not should_quit:
        try:
            main_surface.fill((0, 0, 0))
            player_image = rot_center(player.icon, direction_angle[player.facing])
            main_surface.blit(player_image, (player.x, player.y + ((player.x // tilesize) % 2) * tilesize // 2))
            pygame.display.flip()
            
            action = event_handler.handle_events(player_facing)
            
            if action is None:
                continue
                
            if isinstance(action, RotateAction):
                player.rotate(action.rotate)
            
            elif isinstance(action, MovementAction):
                player.move()
                
            elif isinstance(action, ActionQuit):
                raise SystemExit()
                
        except SystemExit:
            should_quit = True

    pygame.quit()


if __name__ == "__main__":
    main()
