from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

from pygame import Surface

from constants.constants import margin, game_font
from constants.colors import colors
from constants.images import misc_icons
from control_panel import get_keys
from render.utilities import make_text_button, make_arrow_button, render_border

if TYPE_CHECKING:
    from entity import Actor
    from constants.enums import GameStates, KeyMod
    from ui import DisplayInfo


def control_panel_render(console: Surface,
                         key_mod: KeyMod,
                         game_state: GameStates,
                         player: Actor,
                         ui_layout: DisplayInfo,
                         sky: Tuple[int, int, int]) -> None:
    """
    collects lists of arrow keys and text keys from control_panel.py.
    :param console: Surface to blit to
    :param key_mod: current key modifier (shift, command, control, alt, etc.)
    :param game_state: current GameState
    :param player: player Actor
    :param ui_layout: DisplayInfo
    :param sky: current sky color
    :return: None
    """
    control_panel = Surface((ui_layout.control_width, ui_layout.control_height))
    
    arrow_keys, text_keys = get_keys(key_mod, game_state, player)
    
    split = ui_layout.control_width // 4 + margin
    vertical = margin * 2
    spacer = 3
    if arrow_keys:
        for key in arrow_keys:
            vertical = make_arrow_button(panel=control_panel,
                                         split=split,
                                         spacer=spacer,
                                         rotation=key['rotation'],
                                         text=key['text'],
                                         icon=misc_icons['arrow_key'],
                                         font=game_font,
                                         color=colors['mountain'],
                                         vertical=vertical)
    if text_keys:
        for key in text_keys:
            vertical = make_text_button(panel=control_panel,
                                        split=split,
                                        spacer=spacer,
                                        name=key['name'],
                                        text=key['text'],
                                        font=game_font,
                                        color=colors['mountain'],
                                        bkg_color=colors['black'],
                                        vertical=vertical)
    render_border(control_panel, sky)
    console.blit(control_panel, (0, ui_layout.mini_height + ui_layout.status_height))
