from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame.event

from actions import Action, WaitAction, ActionQuit, MovementAction, RotateAction, ArrowAction

if TYPE_CHECKING:
    from engine import Engine

ROTATE_KEYS = {
    pygame.K_LEFT: -1,
    pygame.K_RIGHT: 1
}

MOVEMENT_KEYS = {
    pygame.K_UP: 1
}

WAIT_KEYS = {
    pygame.K_SPACE
}

ATTACK_KEYS = {
    pygame.K_1
}


class EventHandler:
    def __init__(self, engine: Engine):
        self.engine = engine
    
    def handle_events(self):
        raise NotImplementedError()


class MainEventHandler(EventHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
    
    def handle_events(self):
        something_happened = False
        events = pygame.event.get(pump=True)
        if len(events) > 0:
            for event in events:
                action = self.process_event(event)
                if action is None:
                    continue
                try:
                    something_happened = action.perform()
                
                except Exception:
                    return False
            
            if something_happened:
                self.engine.handle_enemy_turns()
    
    def process_event(self, event) -> Optional[Action]:
        player = self.engine.player
        response = None
        if event.type == pygame.QUIT:
            response = ActionQuit(player)
        if event.type == pygame.KEYDOWN:
            if event.key in ROTATE_KEYS:
                response = RotateAction(player, ROTATE_KEYS[event.key])
            elif event.key in MOVEMENT_KEYS:
                response = MovementAction(player)
            elif event.key in ATTACK_KEYS:
                response = ArrowAction(player)
            elif event.key in WAIT_KEYS:
                response = WaitAction(player)
            elif event.key == pygame.K_ESCAPE:
                response = ActionQuit(player)
        
        if response is not None:
            return response


class GameOverEventHandler(EventHandler):
    def handle_events(self):
        something_happened = False
        events = pygame.event.get(pump=True)
        if len(events) > 0:
            for event in events:
                action = self.process_event(event)
                if action is None:
                    continue
                try:
                    something_happened = action.perform()
                
                except Exception:
                    return False
    
    def process_event(self, event) -> Optional[Action]:
        player = self.engine.player
        response = None
        if event.type == pygame.QUIT:
            response = ActionQuit(player)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                response = ActionQuit(player)
        
        if response is not None:
            return response
