from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.constants import margin, game_font
from constants.colors import colors
from constants.images import misc_icons
from render.utilities import make_arrow_button, make_text_button, render_border

if TYPE_CHECKING:
    from ui import DisplayInfo


def main_menu_render(main_display: Surface, ui_layout: DisplayInfo) -> None:
    """
    very simple main menu
    :param main_display: Surface to blit to
    :param ui_layout: DisplayInfo
    """
    control_panel = Surface((ui_layout.control_width, ui_layout.control_height))
    
    arrow_keys = [{'rotation': 0, 'text': 'New Game'},
                  {'rotation': 180, 'text': 'Continue Game'}]
    text_keys = [{'name': 'Esc', 'text': 'Quit'}]
    
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
