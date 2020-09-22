from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame.event
import pygame.mouse as mouse

from actions import Action, AutoAction, ActionQuit, MovementAction, RotateAction, MouseMoveAction, \
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
    pygame.K_DOWN
}

ATTACK_KEYS = {
    # pygame.K_SPACE: "self",
    pygame.K_LEFT: "port",
    pygame.K_RIGHT: "starboard",
    pygame.K_UP: "fore",
    pygame.K_DOWN: "aft"
}

SAIL_KEYS = {
    pygame.K_UP: True,
    pygame.K_DOWN: False
}

MODIFIERS = {
    1: "shift",
    2: "shift",
    256: "alt_option",
    512: "alt_option",
    1024: "control_command",
    2048: "control_command",
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
        # noinspection PyArgumentList
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
            if event.mod == pygame.KMOD_NONE:
                self.engine.key_mod = None
        if event.type == pygame.KEYDOWN:
            if event.mod in MODIFIERS:
                self.engine.key_mod = MODIFIERS[event.mod]
            if self.engine.key_mod == "shift" and event.key in ATTACK_KEYS:
                response = AttackAction(player, ATTACK_KEYS[event.key])
            elif self.engine.key_mod == "control_command" and event.key in SAIL_KEYS:
                response = SailAction(player, SAIL_KEYS[event.key])
            elif self.engine.key_mod == "alt_option":
                pass
            if self.engine.key_mod is None:
                if event.key in ROTATE_KEYS:
                    response = RotateAction(player, ROTATE_KEYS[event.key])
                elif event.key in MOVEMENT_KEYS:
                    response = MovementAction(player)
                elif event.key in WAIT_KEYS:
                    response = AutoAction(player)
                elif event.key == pygame.K_ESCAPE:
                    response = ActionQuit(player)
        
        if event.type == pygame.MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response


class GameOverEventHandler(EventHandler):
    def handle_events(self):
        self.engine.key_mod = None
        # noinspection PyArgumentList
        events = pygame.event.get(pump=True)
        
        if len(events) > 0:
            for event in events:
                action = self.process_event(event)
                if action is None:
                    continue
                try:
                    action.perform()
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
