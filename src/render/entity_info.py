from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants import view_port, game_font, colors, margin
from render.utilities import surface_to_map_coords, render_border, render_simple_bar

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from ui import DisplayInfo


def render_entity_info(console: Surface,
                       game_map: GameMap,
                       player: Actor,
                       mouse_x: int,
                       mouse_y: int,
                       ui: DisplayInfo) -> None:
    """
    renders entity information of things under the mouse
    :param console: surface to blit to
    :param game_map: current GameMap
    :param player: player Actor
    :param mouse_x: int x location of mouse
    :param mouse_y: int y location of mouse
    :param ui: DisplayInfo
    :return: None
    """
    coord_x, coord_y = surface_to_map_coords(mouse_x, mouse_y, player.x)
    trans_x = coord_x + player.x - view_port
    trans_y = coord_y + player.y - view_port
    # print(f"{coord_x}:{coord_y} -> {trans_x}:{trans_y}")
    entities = game_map.get_targets_at_location(trans_x, trans_y)
    entities.extend(game_map.get_items_at_location(trans_x, trans_y))
    visible_entities = []
    for entity in entities:
        if (entity.x, entity.y) in player.view.fov:
            visible_entities.append(entity)
    
    entities_sorted_for_rendering = sorted(
        visible_entities, key=lambda i: i.render_order.value, reverse=True
    )
    
    widths = []
    entity_list = []
    # (x, y) = surface_to_map_coords(mouse_x, mouse_y, player.x)
    # xy = game_font.render(f"{x}:{y}", True, colors['mountain'])
    # widths.append(xy.get_width())
    # entity_list.append((xy, None, None))
    for entity in entities_sorted_for_rendering:
        name = game_font.render(f"{entity.name}", True, colors['mountain'])
        widths.append(name.get_width())
        if entity.fighter:
            entity_list.append((name, entity.fighter.hp, entity.fighter.max_hp))
        else:
            entity_list.append((name, None, None))
    if game_map.in_bounds(trans_x, trans_y) and game_map.terrain[trans_x][trans_y].explored:
        if game_map.terrain[trans_x][trans_y].mist and (trans_x, trans_y) in player.view.fov:
            name = game_font.render(f"Mist", True, colors['mountain'])
            widths.append(name.get_width())
            entity_list.append((name, None, None))
        if game_map.terrain[trans_x][trans_y].decoration:
            name = game_font.render(f"{game_map.terrain[trans_x][trans_y].decoration.capitalize()}",
                                    True, colors['mountain'])
            widths.append(name.get_width())
            entity_list.append((name, None, None))
        name = game_font.render(f"{game_map.terrain[trans_x][trans_y].elevation.name.lower().capitalize()}",
                                True, colors['mountain'])
        entity_list.append((name, None, None))
        widths.append(name.get_width())
    
    # print(f"{coord_x}:{coord_y} -> {trans_x}:{trans_y} ({entity.x}:{entity.y})")
    if len(entity_list) > 0:
        info_surf = Surface((max(widths) + margin * 2,
                             len(entity_list) * game_font.get_height()  # font heights
                             + margin * 2  # borders
                             + (len(entity_list) - 1) * 2))  # spacers between fonts
        info_surf.fill(colors['black'])
        height = 0
        for name, hp, max_hp in entity_list:
            if hp is not None and hp > 0:
                info_surf.blit(render_simple_bar(hp, max_hp, max(widths)),
                               (margin,
                                margin  # border
                                + height * game_font.get_height()  # font height
                                + 2 * height))  # spacer
            info_surf.blit(name, (margin,
                                  margin  # border
                                  + height * game_font.get_height()  # font height
                                  + 2 * height))  # spacer
            height += 1
        
        blit_x = mouse_x + ui.mini_width + margin * 2
        if blit_x + info_surf.get_width() > ui.mini_width + ui.viewport_width:
            blit_x = ui.mini_width + ui.viewport_width - info_surf.get_width() - margin
        blit_y = mouse_y + margin * 2
        if blit_y > ui.viewport_height:
            blit_y = ui.viewport_height - info_surf.get_height() - margin
        
        render_border(info_surf, game_map.engine.time.get_sky_color)
        console.blit(info_surf, (blit_x, blit_y))
