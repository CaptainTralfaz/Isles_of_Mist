from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEMOTION, mouse
from pygame import event as pygame_event

from actions.base.mouse import MouseMoveAction

from actions.base.quit import ActionQuit
from constants.colors import colors
from custom_exceptions import Impossible
from event_handlers.base import EventHandler
from constants.keys import MENU_KEYS

if TYPE_CHECKING:
    from engine import Engine
    from actions.base.base import Action


class MainEventHandler(EventHandler):
    def __init__(self, engine: Engine):
        """
        handles keys and dispatches events for when player is dead
        :param engine: the game Engine
        """
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
            
    def process_event(self, event) -> Optional[Action]:
        player = self.engine.player
        response = None
        if event.type == QUIT:
            response = ActionQuit(player)
        if event.type == KEYDOWN:
            if event.key in MENU_KEYS:
                response = MainMenuAction(event=MENU_KEYS[event.key])
            elif event.key == K_ESCAPE:
                response = ActionQuit(player)
        
        if response is not None:
            return response
