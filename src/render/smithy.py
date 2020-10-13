from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.colors import colors
from constants.constants import game_font, margin
from constants.images import cargo_icons
from constants.stats import item_stats
from render.utilities import render_border, weapon_stats_render

if TYPE_CHECKING:
    from entity import Entity
    from time_of_day import Time
    from ui import DisplayInfo


def smithy_render(console: Surface,
                  player: Entity,
                  time: Time,
                  ui_layout: DisplayInfo) -> None:
    """
    
    :param console: Surface to blit to
    :param player: player Entity
    :param time: current game Time
    :param ui_layout: DisplayInfo
    :return: None
    """
    
    smithy_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    height = margin * 2
    column = 70
    spacer = 35
    
    smithy = player.game_map.port.smithy
    weapon_list = player.broadsides.storage
    smithy_list = smithy.manifest
    
    coins = cargo_icons['coins']
    smithy_surf.blit(coins, (margin * 2, height))
    surf = game_font.render(f"{player.cargo.coins - smithy.temp_coins}", True, colors['mountain'])
    smithy_surf.blit(surf, (spacer, height))
    smithy_surf.blit(coins, (smithy_surf.get_width() - coins.get_width() - margin * 2, height))
    surf = game_font.render(f"{smithy.coins + smithy.temp_coins}", True, colors['mountain'])
    smithy_surf.blit(surf, (smithy_surf.get_width() - surf.get_width() - coins.get_width() - margin * 4, height))
    surf = game_font.render(f"Player Storage", True, colors['mountain'])
    smithy_surf.blit(surf, (spacer + column, height))
    surf = game_font.render(f"Smithy Storage", True, colors['pink'])
    smithy_surf.blit(surf, (spacer + 5 * column, height))
    height += game_font.get_height() + margin
    
    game_font.set_underline(True)
    surf = game_font.render(f"Weapon Name", True, colors['mountain'])
    smithy_surf.blit(surf, (spacer, height))
    c = 3
    for header in ["Wt", "Vol", "Price"]:
        color = colors['pink'] if c > 4 else colors['mountain']
        if c == 5:
            color = colors['cyan']
        surf = game_font.render(f"{header}", True, color)
        smithy_surf.blit(surf, (spacer + c * column - surf.get_width(), height))
        c += 1
    surf = game_font.render(f"Weapon Name", True, colors['pink'])
    smithy_surf.blit(surf, (6 * column, height))
    
    game_font.set_underline(False)
    height += game_font.get_height() + margin
    
    count = 0
    selected_weapon = None
    
    for weapon in weapon_list:
        if count == player.broadsides.selected:
            text_color = colors['black']
            background = colors['mountain']
            selected_weapon = weapon
        else:
            text_color = colors['mountain']
            background = colors['black']
        if weapon in player.broadsides.sell_list:
            surf = game_font.render(f"{weapon.name.capitalize()}", True, text_color, background)
            smithy_surf.blit(surf, (6 * column, height))
        else:
            surf = game_font.render(f"{weapon.name.capitalize()}", True, text_color, background)
            smithy_surf.blit(surf, (spacer, height))
        surf = game_font.render(f"{int(item_stats[weapon.name.lower()]['weight'])}", True, colors['mountain'])
        smithy_surf.blit(surf, (spacer + 3 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[weapon.name.lower()]['volume'])}", True, colors['mountain'])
        smithy_surf.blit(surf, (spacer + 4 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[weapon.name.lower()]['cost'])}", True, colors['cyan'])
        smithy_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
        height += game_font.get_height() + margin
        count += 1
    for weapon in smithy_list:
        if count == player.broadsides.selected:
            text_color = colors['black']
            background = colors['pink']
            selected_weapon = weapon
        else:
            text_color = colors['pink']
            background = colors['black']
        surf = game_font.render(f"{int(item_stats[weapon.name.lower()]['weight'])}", True, colors['mountain'])
        smithy_surf.blit(surf, (spacer + 3 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[weapon.name.lower()]['volume'])}", True, colors['mountain'])
        smithy_surf.blit(surf, (spacer + 4 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[weapon.name.lower()]['cost'])}", True, colors['cyan'])
        smithy_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
        
        if weapon in player.broadsides.buy_list:
            surf = game_font.render(f"{weapon.name.capitalize()}", True, text_color, background)
            smithy_surf.blit(surf, (spacer, height))
        else:
            surf = game_font.render(f"{weapon.name.capitalize()}", True, text_color, background)
            smithy_surf.blit(surf, (6 * column, height))
        height += game_font.get_height() + margin
        count += 1
    
    if selected_weapon is not None:
        stats_surf = weapon_stats_render(selected_weapon, time.get_sky_color)
        smithy_surf.blit(stats_surf, ((ui_layout.viewport_width - stats_surf.get_width()) // 2,
                                      ui_layout.viewport_height - stats_surf.get_height() - margin))

    time.tint_render(smithy_surf)
    render_border(smithy_surf, time.get_sky_color)
    console.blit(smithy_surf, (ui_layout.mini_width, 0))
