from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pygame import QUIT, KEYUP, KEYDOWN, KMOD_NONE, K_ESCAPE
from pygame import event as pygame_event

from constants.keys import MENU_KEYS
from custom_exceptions import Impossible
from game import load_game, Game, new_game

if TYPE_CHECKING:
    pass

QUIT = 512


class MainMenuHandler:
    def __init__(self, shift_mod):
        self.shift_mod = shift_mod
    
    """
    handles keys and dispatches events for the main menu
    """
    
    def handle_events(self, game_display, ui_layout) -> bool:
        # noinspection PyArgumentList
        events = pygame_event.get(pump=True)
        if len(events) > 0:
            for event in events:
                (should_quit, action, number) = self.process_event(event)
                if action is None:
                    return should_quit
                elif action == "LOAD":
                    try:
                        player, engine = load_game(ui_layout=ui_layout, number=number)
                        Game(game_display, engine=engine, number=number).play_game()
                    except FileNotFoundError:
                        return False
                elif action == "NEW":
                    try:
                        player, engine = new_game(ui_layout=ui_layout)
                        Game(game_display, engine=engine, number=number).play_game()
                    except Impossible:
                        return False
    
    def process_event(self, event) -> (bool, Optional[str], Optional[int]):
        action = None
        number = None
        should_quit = False
        if event.type == QUIT:
            should_quit = True
        if event.type == KEYUP:
            if event.mod == KMOD_NONE:
                self.shift_mod = False
        if event.type == KEYDOWN:
            if event.mod in [1, 2]:  # shift is being pressed
                self.shift_mod = True
            if self.shift_mod and event.key in MENU_KEYS:
                action = "LOAD"
                number = MENU_KEYS[event.key].value
                self.shift_mod = False
            elif event.key in MENU_KEYS:
                action = "NEW"
                number = MENU_KEYS[event.key].value
                self.shift_mod = False
            elif event.key == K_ESCAPE:
                should_quit = True
        
        return should_quit, action, number
