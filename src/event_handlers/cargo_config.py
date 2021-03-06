from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pygame import QUIT, KEYUP, KEYDOWN, KMOD_NONE, K_ESCAPE, MOUSEMOTION, mouse
from pygame import event as pygame_event

from actions.base.mouse import MouseMoveAction
from actions.base.quit import ActionQuit
from actions.ship_config.change_select import ChangeSelectionAction
from actions.ship_config.configure import ConfigureAction
from actions.ship_config.confirm import ConfirmAction
from actions.ship_config.exit_config import ExitConfigAction
from components.cargo import Cargo
from constants.enums import GameStates, KeyMod
from constants.keys import MODIFIERS, MENU_KEYS
from custom_exceptions import Impossible
from entity import Entity
from event_handlers.base import EventHandler

if TYPE_CHECKING:
    from engine import Engine
    from actions.base.base import Action


class CargoConfigurationHandler(EventHandler):
    def __init__(self, engine: Engine):
        """
        handles keys and dispatches events for cargo configuration screen
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
                    self.engine.message_log.add_message(e.args[0], text_color='gray')
                    return False
            
            if something_happened:
                if isinstance(something_happened, dict):
                    if something_happened.get('name') == 'Chest':
                        self.engine.game_map.entities.add(
                            Entity(x=something_happened.get('x'),
                                   y=something_happened.get('y'),
                                   elevations=something_happened.get('elevations'),
                                   name=something_happened.get('name'),
                                   icon=something_happened.get('icon'),
                                   cargo=Cargo(max_volume=10,
                                               max_weight=10,
                                               manifest=something_happened.get('cargo'))))
                self.engine.end_turn()
            if self.engine.game_state != GameStates.CARGO_CONFIG:
                self.engine.get_handler()
        return something_happened

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
            if self.engine.key_mod == KeyMod.SHIFT and event.key in MENU_KEYS:
                response = ConfirmAction(player, MENU_KEYS[event.key])
            elif self.engine.key_mod == KeyMod.COMMAND and event.key in MENU_KEYS:
                response = ConfigureAction(player, MENU_KEYS[event.key])
            elif self.engine.key_mod is None:
                if event.key in MENU_KEYS:
                    response = ChangeSelectionAction(player, MENU_KEYS[event.key])
                elif event.key == K_ESCAPE:
                    response = ExitConfigAction(player)
        
        if event.type == MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response
