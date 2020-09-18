from enum import auto, Enum
from math import floor

import pygame.transform as transform
from pygame import Surface, draw

from constants import colors
from constants import view_port, margin, game_font
from utilities import direction_angle


class RenderOrder(Enum):
    CORPSE = auto()
    FLOATER = auto()
    SWIMMER = auto()
    PLAYER = auto()
    FLYER = auto()


def get_rotated_image(image: Surface, facing: int) -> Surface:
    return rot_center(image, direction_angle[facing])


def rot_center(image: Surface, angle: int) -> Surface:
    """
    Rotate an image while keeping its center and size - counter clockwise rotation converted to clockwise
    :param image: Surface icon
    :param angle: how much to rotate image
    :return: rotated icon as a Surface
    """
    orig_rect = image.get_rect()
    rot_image = transform.rotate(image, 360 - angle)  # 360 converts to clockwise
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def render_hp_bar(text: str,
                  current: int,
                  maximum: int,
                  bar_width: int,
                  font_color: str = "bar_text",
                  top_color: str = "bar_filled",
                  bottom_color: str = "bar_empty") -> Surface:
    """
    Renders a visual meter
    :param text: name of the values to render
    :param font_color: text color to render
    :param current: current value
    :param maximum: maximum value
    :param top_color: brighter top color of bar
    :param bottom_color: darker background color of bar
    :param bar_width: width of the bar surface
    :return: Surface to render
    """
    max_bar = Surface((bar_width, game_font.get_height()))
    max_bar.fill(colors[bottom_color])
    if maximum > 0:
        current_bar_length = floor(float(current / maximum * bar_width))
        if current_bar_length < 0:
            current_bar_length = 0
        current_bar = Surface((current_bar_length, game_font.get_height()))
        current_bar.fill(colors[top_color])
        max_bar.blit(current_bar, (0, 0))
    bar_text = game_font.render(f"{text}:", True, colors[font_color])
    bar_nums = game_font.render(f"{current}/{maximum}", True, colors[font_color])
    max_bar.blit(bar_text, (1, 1))
    max_bar.blit(bar_nums, (max_bar.get_width() - bar_nums.get_width(), 1))
    
    return max_bar


def render_simple_bar(current: int,
                      maximum: int,
                      bar_width: int,
                      top_color: str = "bar_filled",
                      bottom_color: str = "bar_empty") -> Surface:
    """
    Renders a visual meter
    :param current: current value
    :param maximum: maximum value
    :param top_color: brighter top color of bar
    :param bottom_color: darker background color of bar
    :param bar_width: width of the bar surface
    :return: Surface to render
    """
    max_bar = Surface((bar_width, game_font.get_height()))
    max_bar.fill(colors[bottom_color])
    if maximum > 0:
        current_bar_length = floor(float(current / maximum * bar_width))
        if current_bar_length < 0:
            current_bar_length = 0
        current_bar = Surface((current_bar_length, game_font.get_height()))
        current_bar.fill(colors[top_color])
        max_bar.blit(current_bar, (0, 0))
    
    return max_bar


def render_entity_info(console, game_map, player, mouse_x, mouse_y, offset):
    coord_x, coord_y = game_map.surface_to_map_coords(mouse_x, mouse_y, player.x)
    entities = game_map.get_targets_at_location(coord_x + player.x - view_port,
                                                coord_y + player.y - view_port,
                                                living_targets=False)
    if player in entities:
        entities.remove(player)
    
    visible_entities = []
    for entity in entities:
        if (entity.x, entity.y) in player.view.fov:
            visible_entities.append(entity)
    
    if len(visible_entities) > 0:
        
        entities_sorted_for_rendering = sorted(
            visible_entities, key=lambda i: i.render_order.value, reverse=True
        )
        
        widths = []
        entity_list = []
        for entity in entities_sorted_for_rendering:
            name = game_font.render(f"{entity.name}", True, colors["white"])
            widths.append(name.get_width())
            if entity.fighter:
                entity_list.append((name, entity.fighter.hp, entity.fighter.max_hp))
            else:
                entity_list.append((name, None, None))
        
        info_surf = Surface((max(widths) + margin * 2,
                             (len(entities) - 1) * 2 + len(entities) * game_font.get_height() + margin * 2))
        render_border(info_surf, colors["white"])
        height = 0
        for name, hp, max_hp in entity_list:
            if hp is not None and hp > 0:
                info_surf.blit(render_simple_bar(hp, max_hp, max(widths)),
                               (margin, margin + height * game_font.get_height() + 2 * height))
            info_surf.blit(name, (margin, margin + height * game_font.get_height() + 2 * height))
            height += 1
        
        console.blit(info_surf, (mouse_x + offset + margin * 2, mouse_y + margin * 2))


def status_panel_render(console: Surface, entity, ui_layout):
    status_panel = Surface((ui_layout.status_width, ui_layout.status_height))
    render_border(status_panel, colors["white"])
    health_bar = render_hp_bar(f"{entity.fighter.name.capitalize()}",
                               entity.fighter.hp,
                               entity.fighter.max_hp,
                               status_panel.get_width() - margin * 2)
    status_panel.blit(health_bar, (margin, margin))
    if entity.sails:
        sail_bar = render_hp_bar(f"{entity.sails.name.capitalize()}",
                                 entity.sails.hp,
                                 entity.sails.max_hp,
                                 status_panel.get_width() - margin * 2)
        status_panel.blit(sail_bar, (margin, margin + margin // 2 + game_font.get_height()))
    console.blit(status_panel, (0, ui_layout.mini_height))
    if entity.crew:
        crew_bar = render_hp_bar(f"{entity.crew.name.capitalize()}",
                                 entity.crew.count,
                                 entity.crew.max_count,
                                 status_panel.get_width() - margin * 2)
        status_panel.blit(crew_bar, (margin, margin + 2 * (margin // 2 + game_font.get_height())))
    console.blit(status_panel, (0, ui_layout.mini_height))
    # TODO render weapons damage/cool-downs, and cargo


def render_border(panel, color):
    """
    Draws a border around the edge of the given panel
    :param panel: Surface to draw on
    :param color: color of the border
    :return: None
    """
    draw.lines(panel, (0, 0, 0), True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 5)  # Black band 5 wide
    draw.lines(panel, color, True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 1)  # White line 1 wide
