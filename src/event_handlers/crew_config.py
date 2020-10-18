from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pygame import QUIT, KEYUP, KEYDOWN, KMOD_NONE, K_ESCAPE, MOUSEMOTION, mouse
from pygame import event as pygame_event

from actions.base.mouse import MouseMoveAction
from actions.base.quit import ActionQuit
from actions.ship_config.change_select import ChangeSelectionAction
from actions.ship_config.configure import ConfigureAction
from actions.ship_config.exit_config import ExitConfigAction
from actions.ship_config.selected import SelectedAction
from constants.enums import GameStates, KeyMod
from constants.keys import MODIFIERS, MENU_KEYS
from custom_exceptions import Impossible
from event_handlers.base import EventHandler

if TYPE_CHECKING:
    from engine import Engine
    from actions.base.base import Action


class CrewConfigurationHandler(EventHandler):
    """
    handles keys and dispatches events for crew configuration screen
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
                    self.engine.message_log.add_message(e.args[0], text_color='gray')
                    return False
            
            if something_happened:
                self.engine.player.view.set_fov()
                if self.engine.player.broadsides:
                    self.engine.player.broadsides.tick_cooldown()
                self.engine.player.crew.tick_cooldowns()
                self.engine.handle_bonus_movement()
                self.engine.handle_enemy_turns()
                self.engine.handle_weather()
                for entity in self.engine.game_map.entities:
                    if entity.is_alive:
                        entity.view.set_fov()
            if self.engine.game_state != GameStates.CREW_CONFIG:
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
            if self.engine.key_mod == KeyMod.SHIFT and event.key in MENU_KEYS:
                response = SelectedAction(player, MENU_KEYS[event.key])
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
