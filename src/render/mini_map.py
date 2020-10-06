from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface, display

from constants import block_size, margin, colors, move_elevations
from render.utilities import render_border

if TYPE_CHECKING:
    from game_map import GameMap
    from ui import DisplayInfo


def mini_map_render(game_map: GameMap, main_display: display, ui_layout: DisplayInfo) -> None:
    """
    renders the mini-map
    :param game_map: current GameMap
    :param main_display: surface to blit to
    :param ui_layout: where to blit the mini-map
    :return: None
    """
    mini_surf = Surface((ui_layout.mini_width, ui_layout.mini_height))
    block = Surface((block_size, block_size))
    mini_block = Surface((block_size // 2, block_size // 2))
    for x in range(game_map.width):
        for y in range(game_map.height):
            if game_map.terrain[x][y].explored:
                block.fill(colors[game_map.terrain[x][y].elevation.name.lower()])
                mini_surf.blit(block, (margin + x * block_size,
                                       margin + y * block_size + (x % 2) * block_size // 2 - 2))
                if game_map.terrain[x][y].decoration:
                    if game_map.terrain[x][y].elevation in move_elevations['land']:
                        color = 'white' if game_map.terrain[x][y].decoration in ["port"] else 'black'
                        block.fill(colors['red'])
                        mini_surf.blit(block, (margin + x * block_size,
                                               margin + y * block_size + (x % 2) * block_size // 2 - 2))
                        mini_block.fill(color)
                        mini_surf.blit(mini_block,
                                       (margin + 1 + x * block_size,
                                        margin + 1 + y * block_size + (x % 2) * block_size // 2 - 2))
                    else:
                        mini_block.fill(colors[game_map.terrain[x][y].decoration])
                        mini_surf.blit(mini_block,
                                       (margin + 1 + x * block_size,
                                        margin + 1 + y * block_size + (x % 2) * block_size // 2 - 2))
    
    for entity in game_map.entities:
        if (entity.x, entity.y) in game_map.engine.player.view.fov \
                and entity.icon is not None:
            if entity == game_map.engine.player:
                block.fill(colors['white'])
            elif entity.is_alive:
                block.fill(colors['red'])
            else:
                block.fill(colors['orange'])
            mini_surf.blit(block, (margin + entity.x * block_size,
                                   margin + entity.y * block_size + (entity.x % 2) * block_size // 2 - 2))
    
    render_border(mini_surf, game_map.engine.time.get_sky_color)
    main_display.blit(mini_surf, (0, 0))
