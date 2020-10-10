from __future__ import annotations

from typing import List, TYPE_CHECKING

from pygame import Surface

from constants.colors import colors
from constants.constants import margin, game_font
from constants.images import misc_icons
from render.utilities import make_arrow_button, make_text_button, render_border

if TYPE_CHECKING:
    from ui import DisplayInfo


def main_menu_render(main_display: Surface,
                     ui_layout: DisplayInfo,
                     available_loads: List[int],
                     shift_mod: bool) -> None:
    """
    very simple main menu
    :param main_display: Surface to blit to
    :param ui_layout: DisplayInfo
    :param available_loads: int List of available save games
    :param shift_mod: boolean True if shift is pressed
    """
    control_panel = Surface((ui_layout.control_width, ui_layout.control_height))
    
    arrow_keys = []
    text_keys = []
    if not shift_mod:
        arrow_keys = [{'rotation': 0, 'text': 'New Game 1'},
                      {'rotation': 90, 'text': 'New Game 2'},
                      {'rotation': 270, 'text': 'New Game 3'},
                      {'rotation': 180, 'text': 'New Game 4'}]
        text_keys = [{'name': 'Shift', 'text': 'Load Game'},
                     {'name': 'Esc', 'text': 'Quit'}]
    else:
        for available in available_loads:
            if available == 1:
                arrow_keys.append({'rotation': 0, 'text': 'Load Game 1'})
            if available == 2:
                arrow_keys.append({'rotation': 90, 'text': 'Load Game 2'})
            if available == 3:
                arrow_keys.append({'rotation': 270, 'text': 'Load Game 3'})
            if available == 4:
                arrow_keys.append({'rotation': 180, 'text': 'Load Game 4'})
    split = ui_layout.control_width // 4 + margin
    vertical = margin * 2
    spacer = 3
    
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
    
    render_border(control_panel, colors['mountain'])
    main_display.blit(control_panel, ((ui_layout.display_width - ui_layout.control_width) // 2,
                                      (ui_layout.display_height - ui_layout.control_height) // 2))
