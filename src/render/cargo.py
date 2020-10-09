from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.colors import colors
from constants.constants import game_font, margin
from constants.images import cargo_icons
from constants.stats import item_stats
from render.utilities import render_border

if TYPE_CHECKING:
    from components.cargo import Cargo
    from time_of_day import Time
    from ui import DisplayInfo


def cargo_render(console: Surface,
                 cargo: Cargo,
                 time: Time,
                 ui_layout: DisplayInfo) -> None:
    """
    
    :param console: Surface to blit to
    :param cargo: player's Cargo component
    :param time: current game Time
    :param ui_layout: DisplayInfo
    :return: None
    """
    
    cargo_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    count = 0
    height = margin * 2
    column = 50
    total_weight = 0
    total_volume = 0
    
    manifest_keys = sorted([key for key in cargo.manifest.keys()], key=lambda i: item_stats[i]['category'].value)
    game_font.set_underline(True)
    spacer = 35
    surf = game_font.render(f"Item Name", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer, height))
    c = 3
    for header in ["Qty", "Wt", "Vol", "T Wt", "T Vol"]:
        surf = game_font.render(f"{header}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + c * column - surf.get_width(), height))
        c += 1
    game_font.set_underline(False)
    height += game_font.get_height() + margin
    for item in manifest_keys:
        if count == cargo.selected:
            text_color = colors['black']
            background = colors['mountain']
        else:
            text_color = colors['mountain']
            background = colors['black']
        cargo_surf.blit(cargo_icons[item], (margin * 2, height))
        surf = game_font.render(f"{item.capitalize()}", True, text_color, background)
        cargo_surf.blit(surf, (spacer, height))
        surf = game_font.render(f"{cargo.manifest[item]}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 3 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[item]['weight'])}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 4 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[item]['volume'])}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[item]['weight'] * cargo.manifest[item])}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
        total_weight += item_stats[item]['weight'] * cargo.manifest[item]
        surf = game_font.render(f"{int(item_stats[item]['volume'] * cargo.manifest[item])}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
        total_volume += item_stats[item]['volume'] * cargo.manifest[item]
        height += game_font.get_height() + margin
        count += 1
    surf = game_font.render(f"Totals", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
    surf = game_font.render(f"{int(total_weight)}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
    surf = game_font.render(f"{int(total_volume)}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
    
    time.tint_render(cargo_surf)
    render_border(cargo_surf, time.get_sky_color)
    console.blit(cargo_surf, (ui_layout.mini_width, 0))
