from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.colors import colors
from constants.constants import game_font, margin
from constants.images import cargo_icons
from constants.stats import item_stats
from render.utilities import render_border

if TYPE_CHECKING:
    from entity import Entity
    from time_of_day import Time
    from ui import DisplayInfo


def cargo_render(console: Surface,
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
    
    cargo_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    height = margin * 2
    column = 70
    spacer = 35

    manifest_keys = sorted([key for key in player.cargo.manifest.keys()],
                           key=lambda i: item_stats[i]['category'].value)
    
    coins = cargo_icons['coins']
    cargo_surf.blit(coins, (margin * 2, height))
    surf = game_font.render(f"{player.cargo.coins}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer, height))
    surf = game_font.render(f"Player Cargo", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + column, height))
    height += game_font.get_height() + margin

    game_font.set_underline(True)
    surf = game_font.render(f"Item Name", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer, height))
    c = 3
    for header in ["Qty", "Wt", "Vol", "T Wt", "T Vol", "Drop"]:
        surf = game_font.render(f"{header}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + c * column - surf.get_width(), height))
        c += 1
    game_font.set_underline(False)
    height += game_font.get_height() + margin
    for item in manifest_keys:
        if item == player.cargo.selected:
            text_color = colors['black']
            background = colors['mountain']
        else:
            text_color = colors['mountain']
            background = colors['black']
        cargo_surf.blit(cargo_icons[item], (margin * 2, height))
        surf = game_font.render(f"{item.capitalize()}", True, text_color, background)
        cargo_surf.blit(surf, (spacer, height))
        surf = game_font.render(f"{player.cargo.manifest[item]}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 3 * column - surf.get_width(), height))
        surf = game_font.render(f"{round(item_stats[item]['weight'])}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 4 * column - surf.get_width(), height))
        surf = game_font.render(f"{round(item_stats[item]['volume'])}", True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
        surf = game_font.render(f"{round(item_stats[item]['weight'] * player.cargo.manifest[item])}",
                                True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
        surf = game_font.render(f"{round(item_stats[item]['volume'] * player.cargo.manifest[item])}",
                                True, colors['mountain'])
        cargo_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
        if item in player.cargo.sell_list.keys():
            surf = game_font.render(f"{player.cargo.sell_list[item]}", True, colors['red'])
            cargo_surf.blit(surf, (spacer + 8 * column - surf.get_width(), height))
        height += game_font.get_height() + margin
    surf = game_font.render(f"Cargo Total", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
    surf = game_font.render(f"{round(player.cargo.weight)}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
    surf = game_font.render(f"{round(player.cargo.volume)}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
    height += game_font.get_height() + margin
    surf = game_font.render(f"Weapon Total", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
    surf = game_font.render(f"{player.broadsides.weight}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
    surf = game_font.render(f"{player.broadsides.volume}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
    height += game_font.get_height() + margin
    surf = game_font.render(f"Crew Total", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
    surf = game_font.render(f"{player.crew.weight}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
    surf = game_font.render(f"{player.crew.volume}", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
    height += game_font.get_height() + margin
    surf = game_font.render(f"Grand Total", True, colors['grass'])
    cargo_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
    total_wt = round(player.crew.weight + player.broadsides.weight + player.cargo.weight)
    color = colors['grass'] if total_wt <= player.cargo.max_weight else colors['red']
    surf = game_font.render(f"{total_wt}", True, color)
    cargo_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
    total_vol = round(player.crew.volume + player.broadsides.volume + player.cargo.volume)
    color = colors['grass'] if total_vol <= player.cargo.max_volume else colors['red']
    surf = game_font.render(f"{total_vol}", True, color)
    cargo_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
    height += game_font.get_height() + margin
    surf = game_font.render(f"Ship Maximum", True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
    surf = game_font.render(f"{player.cargo.max_weight}",
                            True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
    surf = game_font.render(f"{player.cargo.max_volume}",
                            True, colors['mountain'])
    cargo_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))

    time.tint_render(cargo_surf)
    render_border(cargo_surf, time.get_sky_color)
    console.blit(cargo_surf, (ui_layout.mini_width, 0))
