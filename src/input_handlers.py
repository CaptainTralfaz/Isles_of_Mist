from typing import Optional

import pygame.event

from src.actions import Action, ActionQuit, EscapeAction, MovementAction, RotateAction

ROTATE_KEYS = {
    pygame.K_LEFT: -1,
    pygame.K_RIGHT: 1
}

MOVEMENT_KEYS = {
    pygame.K_UP: 1
}


class EventHandler:
    def __init__(self):
        pass
    
    def handle_events(self):
        raise NotImplementedError()


class MainEventHandler:
    def __init__(self):
        super().__init__()
        
    def handle_events(self, direction):
        something_happened = False
        response = None
        event_list = pygame.event.get(pump=True)
        if len(event_list) > 0:
            for event in event_list:
                if event.type == pygame.QUIT:
                    response = ActionQuit()
                if event.type == pygame.KEYDOWN:
                    if event.key in ROTATE_KEYS:
                        response = RotateAction(ROTATE_KEYS[event.key])
                    elif event.key in MOVEMENT_KEYS:
                        response = MovementAction(direction)
                    elif event.key == pygame.K_ESCAPE:
                        response = ActionQuit()

        return response

    def process_event(self, event):
        pass