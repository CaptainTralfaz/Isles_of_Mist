from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.colors import colors
from constants.constants import margin, game_font
from constants.enums import Location
from render.utilities import render_border, render_hp_bar, weapon_stats_render

if TYPE_CHECKING:
    from components.broadsides import Broadsides
    from ui import DisplayInfo
    from time_of_day import Time


def weapon_render(console: Surface,
                  broadsides: Broadsides,
                  time: Time,
                  ui_layout: DisplayInfo) -> None:
    """
    creates display of player's current weapon configuration
    :param console: Surface to blit to
    :param broadsides: player's Broadsides component
    :param time: current game Time
    :param ui_layout: DisplayInfo
    :return: None
    """
    weapon_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    
    count = 0
    height = margin * 2
    weapon_list = broadsides.all_weapons
    
    selected_weapon = None
    for (location, weapon) in weapon_list:
        if count == broadsides.selected:
            text_color = colors['black']
            background = colors['mountain']
            selected_weapon = weapon
        else:
            text_color = colors['mountain']
            background = colors['black']
        item_surf = game_font.render(f"{weapon.name}", True, text_color, background)
        weapon_surf.blit(item_surf, (margin + 100, height))
        hp_surf = render_hp_bar("", weapon.hp, weapon.max_hp, ui_layout.status_width - 2 * margin)
        weapon_surf.blit(hp_surf, (margin + 250, height))
        if location in [Location.PORT, Location.STARBOARD]:
            port_surf = game_font.render(f"{location.name.lower().capitalize()}", True, colors['mountain'])
            weapon_surf.blit(port_surf, ((margin + 100 - port_surf.get_width()) // 2, height))
        height += game_font.get_height() + margin
        count += 1
    
    if selected_weapon is not None:
        stats_surf = weapon_stats_render(selected_weapon, time.get_sky_color)
        
        weapon_surf.blit(stats_surf, ((ui_layout.viewport_width - stats_surf.get_width()) // 2,
                                      ui_layout.viewport_height - stats_surf.get_height() - margin))

    time.tint_render(weapon_surf)
    render_border(weapon_surf, time.get_sky_color)
    console.blit(weapon_surf, (ui_layout.mini_width, 0))
