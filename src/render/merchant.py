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


def merchant_render(console: Surface,
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
    
    merchant_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    height = margin * 2
    column = 70
    spacer = 35
    
    merchant = player.game_map.port.merchant
    sell_manifest = player.cargo.sell_list
    buy_manifest = player.cargo.buy_list
    merchant_manifest = merchant.manifest
    merchant_keys = [key for key in merchant_manifest.keys()]
    manifest_keys = [key for key in player.cargo.manifest.keys()]
    
    all_keys = sorted(list(set(manifest_keys) | set(merchant_keys)),
                      key=lambda i: item_stats[i]['category'].value)
    coins = cargo_icons['coins']
    merchant_surf.blit(coins, (margin * 2, height))
    surf = game_font.render(f"{player.cargo.coins - merchant.temp_coins}", True, colors['mountain'])
    merchant_surf.blit(surf, (spacer, height))
    merchant_surf.blit(coins, (merchant_surf.get_width() - coins.get_width() - margin * 2, height))
    surf = game_font.render(f"{merchant.coins + merchant.temp_coins}", True, colors['mountain'])
    merchant_surf.blit(surf, (merchant_surf.get_width() - surf.get_width() - coins.get_width() - margin * 4, height))
    surf = game_font.render(f"Player Cargo", True, colors['mountain'])
    merchant_surf.blit(surf, (spacer + column, height))
    surf = game_font.render(f"Merchant Cargo", True, colors['pink'])
    merchant_surf.blit(surf, (spacer + 5 * column, height))
    height += game_font.get_height() + margin
    
    game_font.set_underline(True)
    surf = game_font.render(f"Cargo Item Name", True, colors['mountain'])
    merchant_surf.blit(surf, (spacer, height))
    c = 3
    for header in ["Qty", "Price", "Sell", "Qty", "Buy"]:
        color = colors['pink'] if c > 4 else colors['mountain']
        if c == 4:
            color = colors['cyan']
        surf = game_font.render(f"{header}", True, color)
        merchant_surf.blit(surf, (spacer + c * column - surf.get_width(), height))
        c += 1
    game_font.set_underline(False)
    
    height += game_font.get_height() + margin
    for item in all_keys:
        if item == player.cargo.selected:
            text_color = colors['black']
            background = colors['mountain']
        else:
            text_color = colors['mountain']
            background = colors['black']
        merchant_surf.blit(cargo_icons[item], (margin * 2, height))
        surf = game_font.render(f"{item.capitalize()}", True, text_color, background)
        merchant_surf.blit(surf, (spacer, height))
        if item in manifest_keys:
            surf = game_font.render(f"{player.cargo.manifest[item]}", True, colors['mountain'])
            merchant_surf.blit(surf, (spacer + 3 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[item]['cost'])}", True, colors['cyan'])
        merchant_surf.blit(surf, (spacer + 4 * column - surf.get_width(), height))
        if item in sell_manifest.keys():
            surf = game_font.render(f"{sell_manifest[item]}", True, colors['grass'])
            merchant_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
        if item in merchant_manifest.keys():
            surf = game_font.render(f"{merchant_manifest[item]}", True, colors['pink'])
            merchant_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
        if item in buy_manifest.keys():
            surf = game_font.render(f"{buy_manifest[item]}", True, colors['red'])
            merchant_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
        height += game_font.get_height() + margin
    
    time.tint_render(merchant_surf)
    render_border(merchant_surf, time.get_sky_color)
    console.blit(merchant_surf, (ui_layout.mini_width, 0))
