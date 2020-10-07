from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pygame import QUIT, KEYUP, KEYDOWN, KMOD_NONE, K_ESCAPE, MOUSEMOTION, mouse
from pygame import event as pygame_event

from actions.mouse import MouseMoveAction
from actions.quit import ActionQuit
from actions.ship_config.configure import ConfigureAction
from constants.colors import colors
from custom_exceptions import Impossible
from constants.enums import GameStates, KeyMod
from event_handlers.base import EventHandler
from constants.keys import MODIFIERS, MENU_KEYS

if TYPE_CHECKING:
    from engine import Engine
    from actions.base import Action


class GameOverEventHandler(EventHandler):
    """
    handles keys and dispatches events for when player is dead
    :param engine: the game Engine
    """
    def __init__(self, engine: Engine):
        super().__init__(engine)
    
    def handle_events(self):
        something_happened = False
        # noinspection PyArgumentList
        events = pygame_event.get(pump=True)
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
                self.engine.get_handler()
    
    def process_event(self, event) -> Optional[Action]:
        player = self.engine.player
        response = None
        if event.type == QUIT:
            response = ActionQuit(player)
        if event.type == KEYUP:
            if event.mod == KMOD_NONE:
                self.engine.key_mod = None
        if event.type == KEYDOWN:
            if event.mod in MODIFIERS:
                self.engine.key_mod = MODIFIERS[event.mod]
            if self.engine.key_mod == KeyMod.COMMAND and event.key in MENU_KEYS:
                response = ConfigureAction(player, MENU_KEYS[event.key], self.engine.game_state)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    response = ActionQuit(player)
        
        if event.type == MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response
