from enum import auto, Enum
from math import floor

import pygame.transform as transform
from pygame import Surface, font, draw

from colors import colors
from utilities import direction_angle, surface_to_map_coords

font.init()

game_font = font.Font('freesansbold.ttf', 16)


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


def render_bar(text: str,
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


def render_entity_info(console, game_map, fov, mouse_x, mouse_y):
    coord_x, coord_y = surface_to_map_coords(mouse_x, mouse_y)
    entities = game_map.get_targets_at_location(coord_x, coord_y, living_targets=False)
    visible_entities = []
    for entity in entities:
        if (entity.x, entity.y) in fov:
            visible_entities.append(entity)
    
    if len(visible_entities) > 0:
        
        entities_sorted_for_rendering = sorted(
            visible_entities, key=lambda i: i.render_order.value, reverse=True
        )
        
        widths = []
        entity_names = []
        for entity in entities_sorted_for_rendering:
            name = game_font.render(f"{entity.name}", True, colors["white"])
            widths.append(name.get_width())
            entity_names.append(name)
        
        info_surf = Surface((max(widths) + 10, len(entities) * game_font.get_height() + 10))
        render_border(info_surf, colors["white"])
        height = 0
        for name in entity_names:
            info_surf.blit(name, (5, 5 + height * game_font.get_height()))
            height += 1
        
        console.blit(info_surf, (mouse_x + 16, mouse_y + 16))


def render_border(panel, color):
    """
    Draws a border around the edge of the given panel
    :param panel: Surface to draw on
    :param color: color of the border
    :return: None
    """
    draw.lines(panel, color, True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 1)
