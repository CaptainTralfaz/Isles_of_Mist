from __future__ import annotations

from math import floor
from typing import List, Tuple, TYPE_CHECKING

import pygame.transform as transform
from pygame import Surface, draw, BLEND_RGBA_MULT, BLEND_RGBA_ADD

from constants.constants import margin, tile_size, view_port, game_font
from constants.colors import colors
from constants.images import entity_icons
from utilities import direction_angle

if TYPE_CHECKING:
    from pygame.font import Font
    from camera import Camera
    from entity import Actor


def get_rotated_image(image: Surface, facing: int) -> Surface:
    """
    rotates an image / sprite to its current facing
    :param image: original Surface to rotate
    :param facing: current facing of Entity
    :return: rotated Surface
    """
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


def surface_to_map_coords(x: int, y: int, player_x: int) -> Tuple[int, int]:
    """
    translate mouse coordinates to game_map coordinates
    :param x: int x mouse coordinate
    :param y: int x mouse coordinate
    :param player_x: current x value of player position
    :return: x, y coordinates of game_map hex
    """
    half_tile_size = tile_size // 2
    x_grid = x // tile_size
    
    y_grid = (y - margin - margin // 2
              # even and odd
              + half_tile_size * (player_x % 2)
              # odd viewport
              - (view_port % 2) * half_tile_size
              + (view_port % 2) * half_tile_size * ((x_grid + player_x) % 2)
              # even viewport
              - ((view_port + 1) % 2) * half_tile_size * ((x_grid + player_x) % 2)
              ) // tile_size
    return x_grid, y_grid


def map_to_surface_coords(x: int,
                          y: int,
                          left: int,
                          top: int,
                          overlap: int,
                          player: Actor,
                          camera: Camera,
                          entity=None) -> Tuple[int, int]:
    """
    translates map coordinates to viewport coordinates
    :param x: int x of game_map coordinates
    :param y: int x of game_map coordinates
    :param left: int left edge coordinate of viewport
    :param top: int top edge of coordinate of viewport
    :param overlap: number of hexes rendered beyond viewport
    :param player: the player (for x/y coordinates
    :param camera: current camera location
    :param entity: entity sprites are smaller than terrain hexes, so adjust placement
    :return: x, y coordinates to render on viewport
    """
    new_x = (x - left - overlap) * tile_size - 2 * margin + player.x * tile_size - camera.x
    new_y = ((y - top - overlap) * tile_size + (x % 2) * tile_size // 2 - 2 * margin
             - (player.x + 1) % 2 * tile_size // 2 + tile_size // 2
             + player.y * tile_size - camera.y)
    if entity:
        new_x += margin
        new_y += 2 * margin
    return new_x, new_y


def make_arrow_button(panel: Surface,
                      split: int,
                      spacer: int,
                      rotation: int,
                      text: str,
                      icon: Surface,
                      font: Font,
                      color: Tuple[int, int, int],
                      vertical: int) -> int:
    """
    Creates and renders an arrow button and description in control panel
    :param panel: Surface to render on
    :param split: vertical line - render button on one side, text on the other
    :param spacer: spacing between font heights
    :param rotation: degrees to rotate icon
    :param text: str action corresponding to the arrow button
    :param icon: arrow icon
    :param font: Font for rendering name
    :param color: color of the text to render
    :param vertical: int y value to render at
    :return: current vertical value
    """
    panel.blit(rot_center(image=icon, angle=rotation),
               (split - spacer - icon.get_width(), vertical))
    panel.blit(font.render(text, True, color),
               (split + spacer, vertical + 1))
    vertical += font.get_height() + spacer
    return vertical


def make_text_button(panel: Surface,
                     split: int,
                     spacer: int,
                     name: str,
                     text: str,
                     font: Font,
                     color: Tuple[int, int, int],
                     bkg_color: Tuple[int, int, int],
                     vertical: int) -> int:
    """
    Creates and renders the key button and description in control panel
    :param panel: Surface to render on
    :param split: vertical line - render button on one side, text on the other
    :param spacer: spacing between font heights
    :param name: str name of the key
    :param text: str action corresponding to the text button
    :param font: Font for rendering name and key
    :param color: color of the text to render
    :param bkg_color: background color (for reversing the colors of the key name)
    :param vertical: int y value to render at
    :return: current vertical value
    """
    key_text = font.render(name, True, bkg_color)
    w, h = font.size(name)
    key_surf = Surface((w + 3, h))
    key_surf.fill(color)
    key_surf.blit(key_text, (1, 1))
    panel.blit(key_surf, (split - spacer - key_surf.get_width(), vertical))
    panel.blit(font.render(text, True, color),
               (split + spacer, vertical + 1))
    vertical += font.get_height() + spacer
    return vertical


def render_border(panel: Surface, color: Tuple[int, int, int]) -> None:
    """
    Draws a border around the edge of the given panel
    :param panel: Surface to draw on
    :param color: color of the border
    :return: None
    """
    draw.lines(panel, colors['black'], True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 5)  # Black band 5 wide
    draw.lines(panel, color, True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 1)  # White line 1 wide


def render_hp_bar(text: str,
                  current: int,
                  maximum: int,
                  bar_width: int,
                  font_color: str = "mountain",
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
    bar_text = game_font.render(f"{text}", True, colors[font_color])
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


def create_ship_icon(entity: Actor) -> Surface:
    """
    Create ship icon from a sprite sheet
    :param entity: Entity's icon to be generated
    :return: created ship icon
    """
    wake = (0, 0, tile_size, tile_size)
    hull = (0, tile_size, tile_size, tile_size)
    sail = (tile_size, tile_size, tile_size, tile_size)
    emblem = (tile_size, 0, tile_size, tile_size)
    icon = Surface((tile_size, tile_size))
    icon.set_colorkey(colors['black'])
    
    sheet = entity_icons[entity.icon]
    # if moving blit wake, but for now, if sail raised
    if entity.sails.raised:
        icon.blit(sheet.subsurface(wake), (0, 0))  # wake
    icon.blit(sheet.subsurface(hull), (0, 0))  # hull
    if entity.sails.raised:
        icon.blit(sheet.subsurface(sail), (0, 0))  # sail
        # if entity.affiliation:
        #     emblem_sheet = sheet.subsurface(emblem)
        #     # colorize it somehow ?
        #     icon.blit(emblem_sheet, (0, 0))  # emblem
        icon.blit(sheet.subsurface(emblem), (0, 0))  # emblem
    
    return icon


def colorize(image: Surface, new_color: List[int]):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color,
        preserving the per-pixel alphas of the original).
    :param image: Surface to create a colorized copy of
    :param new_color: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()
    
    # zero out RGB values
    image.fill((0, 0, 0, 255), None, BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(new_color[0:3] + (0,), None, BLEND_RGBA_ADD)
    
    return image
