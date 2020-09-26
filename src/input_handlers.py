from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame.event
import pygame.mouse as mouse

from actions import Action, AutoAction, ActionQuit, MovementAction, RotateAction, MouseMoveAction, \
    ShipAction, AttackAction, PortAction
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

AUTO_KEYS = {
    pygame.K_DOWN
}

ATTACK_KEYS = {
    pygame.K_LEFT: "port",
    pygame.K_RIGHT: "starboard",
    pygame.K_UP: "fore",
    pygame.K_DOWN: "aft",
}

PORT_KEYS = {
    pygame.K_UP: "sails",
    pygame.K_RIGHT: "shipyard",
    pygame.K_LEFT: "crew",
    pygame.K_DOWN: "weapons",
}

SHIP_KEYS = {
    pygame.K_UP: "sail",
}

MODIFIERS = {
    1: "targeting",
    2: "targeting",
    256: "alt_option",
    512: "alt_option",
    1024: "ship",
    2048: "ship",
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
                    self.engine.message_log.add_message(e.args[0], colors['gray'])
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
        port = (player.x, player.y) == self.engine.game_map.port
        response = None
        if event.type == pygame.QUIT:
            response = ActionQuit(player)
        if event.type == pygame.KEYUP:
            if event.mod == pygame.KMOD_NONE:
                self.engine.key_mod = None
        if event.type == pygame.KEYDOWN:
            if event.mod in MODIFIERS:
                self.engine.key_mod = MODIFIERS[event.mod]
            if self.engine.key_mod == "targeting" and (event.key in ATTACK_KEYS or event.key in PORT_KEYS):
                if port:
                    response = PortAction(player, PORT_KEYS[event.key])
                else:
                    response = AttackAction(player, ATTACK_KEYS[event.key])
            elif self.engine.key_mod == "ship" and event.key in SHIP_KEYS:
                response = ShipAction(player, SHIP_KEYS[event.key])
            elif self.engine.key_mod == "alt_option":
                pass
            if self.engine.key_mod is None:
                if event.key in ROTATE_KEYS:
                    response = RotateAction(player, ROTATE_KEYS[event.key])
                elif event.key in MOVEMENT_KEYS:
                    response = MovementAction(player)
                elif event.key in AUTO_KEYS:
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
