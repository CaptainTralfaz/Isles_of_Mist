from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame.event
import pygame.mouse as mouse

from actions import Action, WaitAction, ActionQuit, MovementAction, RotateAction, MouseMoveAction, \
    SailAction, AttackAction
from constants import colors
from custom_exceptions import Impossible

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
    pygame.K_SPACE: "arrow",
    pygame.K_LEFT: "port",
    pygame.K_RIGHT: "starboard",
    pygame.K_UP: "fore",
    pygame.K_DOWN: "aft"
}

SAIL_KEYS = {
    pygame.K_u: True,
    pygame.K_i: False
}

MODIFIERS = {
    1,  # shift (left)
    2,  # shift (right)
    64,  # control
    256,  # opt / alt (left)
    512,  # opt / alt (right)
    1024,  # command (left)
    2048  # command (right)
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
                
                except Impossible as e:
                    self.engine.message_log.add_message(e.args[0], colors["impossible"])
                    return False
            
            if something_happened:
                self.engine.player.view.set_fov()
                self.engine.handle_bonus_movement()
                self.engine.handle_enemy_turns()
                self.engine.handle_weather()
                for entity in self.engine.game_map.entities:
                    if entity.is_alive:
                        entity.view.set_fov()
    
    def process_event(self, event) -> Optional[Action]:
        player = self.engine.player
        response = None
        if event.type == pygame.QUIT:
            response = ActionQuit(player)
        if event.type == pygame.KEYUP:
            self.engine.key_mod = None
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_mods() in MODIFIERS:
                self.engine.key_mod = pygame.key.get_mods()
            if self.engine.key_mod in [1, 2] and event.key in ATTACK_KEYS:
                response = AttackAction(player, ATTACK_KEYS[event.key])
            if not self.engine.key_mod:
                if event.key in ROTATE_KEYS:
                    response = RotateAction(player, ROTATE_KEYS[event.key])
                elif event.key in MOVEMENT_KEYS:
                    response = MovementAction(player)
                elif event.key in SAIL_KEYS:
                    response = SailAction(player, SAIL_KEYS[event.key])
                elif event.key in WAIT_KEYS:
                    response = WaitAction(player)
                elif event.key == pygame.K_ESCAPE:
                    response = ActionQuit(player)
        
        if event.type == pygame.MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
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
        
        if event.type == pygame.MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response
