from enum import auto, Enum

import pygame.transform as transform
from pygame import Surface

from utilities import direction_angle


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


class RenderOrder(Enum):
    CORPSE = auto()
    FLOATER = auto()
    SWIMMER = auto()
    FLYER = auto()
