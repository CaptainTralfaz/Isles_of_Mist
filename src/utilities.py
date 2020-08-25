from src.tile import Elevation
from src.game_map import GameMap
from typing import List, Tuple


direction_angle = [0, 60, 120, 180, 240, 300]


class Cube:
    def __init__(self, x: int, y: int, z: int):
        """
        Container to hold cubic values in an (x, y, z) coordinate system
        :param x: int x value of an (x, y, z) coordinate system
        :param y: int y value of an (x, y, z) coordinate system
        :param z: int z value of an (x, y, z) coordinate system
        """
        self.x = x
        self.y = y
        self.z = z


"""
Returns the neighbor cube in the given direction
"""
cube_directions = [Cube(0, 1, -1),  # (0) Up
                   Cube(1, 0, -1),  # (1) upper right
                   Cube(1, -1, 0),  # (2) lower right
                   Cube(0, -1, 1),  # (3) Down
                   Cube(-1, 0, 1),  # (4) lower left
                   Cube(-1, 1, 0)  # (5) upper left
                   ]


class Hex:
    def __init__(self, column: int, row: int):
        """
        Container to hold a tile (x, y) coordinate
        :param column: int x value of an (x, y) coordinate system
        :param row: int y value of an (x, y) coordinate system
        """
        self.col = column
        self.row = row


def cube_to_hex(cube: Cube) -> Hex:
    """
    Convert cube coordinates to hexagonal (col, row) coordinates (directly translates to (x, y) map coordinates)
    :param cube: tile in cubic coordinates
    :return: tile in hexagonal coordinates
    """
    col = cube.x
    row = cube.z + (cube.x - cube.x % 2) // 2
    return Hex(col, row)


def hex_to_cube(hexagon: Hex) -> Cube:
    """
    Convert hexagonal (col, row) coordinates to cubic coordinates (easier to work with than (x, y) map coordinates)
    :param hexagon: tile in hexagonal coordinates
    :return: tile in cubic coordinates
    """
    x = hexagon.col
    z = hexagon.row - (hexagon.col - hexagon.col % 2) // 2
    y = -x - z
    return Cube(x, y, z)


def cube_add(cube1, cube2) -> Cube:
    """
    adds the cubic coordinate values of two cubes
    :param cube1: first cube
    :param cube2: second cube
    :return: cubic coordinates
    """
    return Cube(x=cube1.x + cube2.x, y=cube1.y + cube2.y, z=cube1.z + cube2.z)


def cube_direction(direction) -> Cube:
    """
    Returns neighboring cubic relational values in a given hex direction
    :param direction: int direction
    :return: cubic relational values of neighbor in given hex direction
    """
    return cube_directions[direction]


def cube_neighbor(cube, direction) -> Cube:
    """
    Returns neighboring cubic coordinates in a given hex direction
    :param cube: cubic coordinates
    :param direction: int direction
    :return: cubic coordinates of neighbor in the given direction
    """
    return cube_add(cube1=cube, cube2=cube_direction(direction))


def get_hex_water_neighbors(game_map: GameMap, x: int, y: int) -> List[Tuple[int, int]]:
    """
    Returns neighboring water tiles of a given (x, y) map coordinate
    :param game_map: GameMap
    :param x: int x of the game map coordinate
    :param y: int y of the game map coordinate
    :return: list of tile coordinate (x, y) tuples
    """
    neighbors = []
    for direction in cube_directions:
        start_cube = hex_to_cube(hexagon=Hex(column=x, row=y))
        neighbor_hex = cube_to_hex(cube=cube_add(cube1=start_cube, cube2=direction))
        if game_map.in_bounds(neighbor_hex.col, neighbor_hex.row) \
                and game_map.terrain[neighbor_hex.col][neighbor_hex.row] < Elevation.BEACH:
            neighbors.append((neighbor_hex.col, neighbor_hex.row))
    return neighbors
