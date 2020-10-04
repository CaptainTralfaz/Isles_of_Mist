from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame.event
import pygame.mouse as mouse

from actions import Action, AutoAction, ActionQuit, MovementAction, RotateAction, MouseMoveAction, \
    ShipAction, AttackAction, PortAction, RepairAction, ExitMenuAction, ConfigureAction, \
    SelectedAction, ChangeSelectionAction
from constants import colors, Location
from custom_exceptions import Impossible
from game_states import GameStates

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
    pygame.K_UP: Location.FORE,
    pygame.K_RIGHT: Location.STARBOARD,
    pygame.K_LEFT: Location.PORT,
    pygame.K_DOWN: Location.AFT,
}

PORT_KEYS = {
    pygame.K_UP: "shipyard",  # ship upgrades (crew capacity, cargo weight/volume, sails
    pygame.K_RIGHT: "merchant",  # buy/sell cargo
    pygame.K_LEFT: "barracks",  # hire/release crew
    pygame.K_DOWN: "tavern",  # buy/sell weapons
}

REPAIR_KEYS = {
    pygame.K_UP: "sails",
    pygame.K_RIGHT: "shipyard",
    pygame.K_LEFT: "crew",  # TODO: remove this once "hire crew" implemented in port_keys
    pygame.K_DOWN: "engineer",
}

SHIP_KEYS = {
    pygame.K_UP: "sails",
    pygame.K_RIGHT: "cargo",
    pygame.K_LEFT: "crew",
    pygame.K_DOWN: "weapons",
}

CONFIGURE_KEYS = {  # TODO: change arrow keys to enum??
    pygame.K_UP: "up",
    pygame.K_RIGHT: "right",
    pygame.K_LEFT: "left",
    pygame.K_DOWN: "down",
}

MODIFIERS = {
    1: "shift",
    2: "shift",
    256: "option",
    512: "option",
    1024: "command",
    2048: "command",
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
                if self.engine.player.broadsides:
                    self.engine.player.broadsides.tick_cooldown()
                self.engine.handle_bonus_movement()
                self.engine.handle_enemy_turns()
                self.engine.handle_weather()
                for entity in self.engine.game_map.entities:
                    if entity.is_alive:
                        entity.view.set_fov()
            if self.engine.game_state != GameStates.ACTION:
                get_handler(self.engine)
    
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
            if self.engine.key_mod == "shift" and (event.key in ATTACK_KEYS or event.key in REPAIR_KEYS):
                if port:
                    response = RepairAction(player, REPAIR_KEYS[event.key])
                else:
                    response = AttackAction(player, ATTACK_KEYS[event.key])
            elif self.engine.key_mod == "command" and event.key in SHIP_KEYS:
                response = ShipAction(player, SHIP_KEYS[event.key], self.engine.game_state)
            elif port and self.engine.key_mod == "option" and event.key in PORT_KEYS:
                response = PortAction(player, PORT_KEYS[event.key])
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


class WeaponConfigurationHandler(EventHandler):
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
                if self.engine.player.broadsides:
                    self.engine.player.broadsides.tick_cooldown()
                self.engine.handle_bonus_movement()
                self.engine.handle_enemy_turns()
                self.engine.handle_weather()
                for entity in self.engine.game_map.entities:
                    if entity.is_alive:
                        entity.view.set_fov()
            if self.engine.game_state != GameStates.WEAPON_CONFIG:
                get_handler(self.engine)
    
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
            if self.engine.key_mod == "shift" and event.key in CONFIGURE_KEYS:
                response = SelectedAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
            elif self.engine.key_mod == "command" and event.key in CONFIGURE_KEYS:
                response = ConfigureAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
            elif self.engine.key_mod is None:
                if event.key in CONFIGURE_KEYS:
                    response = ChangeSelectionAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
                elif event.key == pygame.K_ESCAPE:
                    response = ExitMenuAction(player)
        
        if event.type == pygame.MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response


class CrewConfigurationHandler(EventHandler):
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
                if self.engine.player.broadsides:
                    self.engine.player.broadsides.tick_cooldown()
                self.engine.handle_bonus_movement()
                self.engine.handle_enemy_turns()
                self.engine.handle_weather()
                for entity in self.engine.game_map.entities:
                    if entity.is_alive:
                        entity.view.set_fov()
            if self.engine.game_state != GameStates.CREW_CONFIG:
                get_handler(self.engine)
    
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
            if self.engine.key_mod == "shift" and event.key in CONFIGURE_KEYS:
                response = SelectedAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
            elif self.engine.key_mod == "command" and event.key in CONFIGURE_KEYS:
                response = ConfigureAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
            elif self.engine.key_mod is None:
                if event.key in CONFIGURE_KEYS:
                    response = ChangeSelectionAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
                elif event.key == pygame.K_ESCAPE:
                    response = ExitMenuAction(player)
        
        if event.type == pygame.MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response


class CargoConfigurationHandler(EventHandler):
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
                if self.engine.player.broadsides:
                    self.engine.player.broadsides.tick_cooldown()
                self.engine.handle_bonus_movement()
                self.engine.handle_enemy_turns()
                self.engine.handle_weather()
                for entity in self.engine.game_map.entities:
                    if entity.is_alive:
                        entity.view.set_fov()
            if self.engine.game_state != GameStates.CARGO_CONFIG:
                get_handler(self.engine)
    
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
            if self.engine.key_mod == "shift" and event.key in CONFIGURE_KEYS:
                response = SelectedAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
            elif self.engine.key_mod == "command" and event.key in CONFIGURE_KEYS:
                response = ConfigureAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
            elif self.engine.key_mod is None:
                if event.key in CONFIGURE_KEYS:
                    response = ChangeSelectionAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
                elif event.key == pygame.K_ESCAPE:
                    response = ExitMenuAction(player)
        
        if event.type == pygame.MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response


class GameOverEventHandler(EventHandler):
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
                pass
            if self.engine.game_state != GameStates.CARGO_CONFIG:
                get_handler(self.engine)
    
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
            if self.engine.key_mod == "command" and event.key in CONFIGURE_KEYS:
                response = ConfigureAction(player, CONFIGURE_KEYS[event.key], self.engine.game_state)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    response = ActionQuit(player)
        
        if event.type == pygame.MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response


def get_handler(engine):
    if engine.game_state == GameStates.ACTION:
        engine.event_handler = MainEventHandler(engine)
    elif engine.game_state == GameStates.WEAPON_CONFIG:
        engine.event_handler = WeaponConfigurationHandler(engine)
    elif engine.game_state == GameStates.CREW_CONFIG:
        engine.event_handler = CrewConfigurationHandler(engine)
    elif engine.game_state == GameStates.CARGO_CONFIG:
        engine.event_handler = CargoConfigurationHandler(engine)
    elif engine.game_state == GameStates.PLAYER_DEAD:
        engine.event_handler = GameOverEventHandler(engine)
