from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.colors import colors
from constants.constants import game_font, margin
from constants.enums import GameStates
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
    sell_manifest = {}
    if player.game_map.engine.game_state == GameStates.MERCHANT:
        sell_manifest = player.game_map.port.merchant.manifest
    elif player.game_map.engine.game_state == GameStates.MERCHANT:
        sell_manifest = player.game_map.port.smithy.manifest

    merchant_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    count = 0
    height = margin * 2
    column = 70
    
    manifest_keys = sorted([key for key in player.cargo.manifest.keys()],
                           key=lambda i: item_stats[i]['category'].value)
    game_font.set_underline(True)
    spacer = 35
    surf = game_font.render(f"Cargo Item Name", True, colors['mountain'])
    merchant_surf.blit(surf, (spacer, height))
    c = 3
    for header in ["Qty", "Sell", "Price", "Qty", "Buy"]:
        surf = game_font.render(f"{header}", True, colors['mountain'])
        merchant_surf.blit(surf, (spacer + c * column - surf.get_width(), height))
        c += 1
    game_font.set_underline(False)
    height += game_font.get_height() + margin
    for item in manifest_keys:
        if count == player.cargo.selected:
            text_color = colors['black']
            background = colors['mountain']
        else:
            text_color = colors['mountain']
            background = colors['black']
        merchant_surf.blit(cargo_icons[item], (margin * 2, height))
        surf = game_font.render(f"{item.capitalize()}", True, text_color, background)
        merchant_surf.blit(surf, (spacer, height))
        surf = game_font.render(f"{player.cargo.manifest[item]}", True, colors['mountain'])
        merchant_surf.blit(surf, (spacer + 3 * column - surf.get_width(), height))
        surf = game_font.render(f"{int(item_stats[item]['cost'])}", True, colors['mountain'])
        merchant_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
        if item in sell_manifest.keys():
            surf = game_font.render(f"{sell_manifest[item]}", True, colors['mountain'])
            merchant_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
        height += game_font.get_height() + margin
        count += 1

        # surf = game_font.render(f"{int(item_stats[item]['volume'])}", True, colors['mountain'])
        # merchant_surf.blit(surf, (spacer + 5 * column - surf.get_width(), height))
        # surf = game_font.render(f"{int(item_stats[item]['weight'] * player.cargo.manifest[item])}",
        #                         True, colors['mountain'])
        # merchant_surf.blit(surf, (spacer + 6 * column - surf.get_width(), height))
        # surf = game_font.render(f"{int(item_stats[item]['volume'] * player.cargo.manifest[item])}",
        #                         True, colors['mountain'])
        # merchant_surf.blit(surf, (spacer + 7 * column - surf.get_width(), height))
    
    time.tint_render(merchant_surf)
    render_border(merchant_surf, time.get_sky_color)
    console.blit(merchant_surf, (ui_layout.mini_width, 0))
