from random import randint
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


def cube_direction(direction: int) -> Cube:
    """
    Returns neighboring cubic relational values in a given hex direction
    :param direction: int direction
    :return: cubic relational values of neighbor in given hex direction
    """
    return cube_directions[direction]


def cube_neighbor(cube: Cube, direction: int) -> Cube:
    """
    Returns neighboring cubic coordinates in a given hex direction
    :param cube: cubic coordinates
    :param direction: int direction
    :return: cubic coordinates of neighbor in the given direction
    """
    return cube_add(cube1=cube, cube2=cube_direction(direction))


def get_neighbor(x: int, y: int, direction: int) -> Tuple[int, int]:
    neighbor = cube_to_hex(cube_neighbor(hex_to_cube(Hex(x, y)), direction))
    return neighbor.col, neighbor.row


def cube_distance(cube1: Cube, cube2: Cube) -> int:
    """
    Distance between two tiles in cubic coordinates
    :param cube1: origin cube
    :param cube2: target cube
    :return: int distance between cubes
    """
    return max(abs(cube1.x - cube2.x), abs(cube1.y - cube2.y), abs(cube1.z - cube2.z))


def get_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Distance between two tiles on hex grid
    :param x1: x coordinate of source hex
    :param y1: y coordinate of source hex
    :param x2: x coordinate of destination hex
    :param y2: y coordinate of destination hex
    :return: int distance between hexes
    """
    return cube_distance(hex_to_cube(Hex(x1, y1)), hex_to_cube(Hex(x2, y2)))


def cube_line_draw(cube1: Cube, cube2: Cube) -> List[Cube]:
    """
    function to return a list of cube coordinates in a line from cube1 to cube2
    :param cube1: starting cube coordinates
    :param cube2: ending cube coordinates
    :return: list of cubes from cube1 to cube2 inclusive
    """
    n = cube_distance(cube1=cube1, cube2=cube2)
    cube_line = []
    for i in range(0, n + 1):
        cube_line.append(cube_round(cube=cube_lerp(a=cube1, b=cube2, t=1.0 / n * i)))
    return cube_line[1:]


def cube_round(cube: Cube) -> Cube:
    """
    cubic line drawing helper
    """
    rx = round(cube.x)
    ry = round(cube.y)
    rz = round(cube.z)
    
    x_diff = abs(rx - cube.x)
    y_diff = abs(ry - cube.y)
    z_diff = abs(rz - cube.z)
    
    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return Cube(rx, ry, rz)


def lerp(a: int, b: int, t):
    """
    cubic line drawing helper
    """
    return a + (b - a) * t


def cube_lerp(a: Cube, b: Cube, t) -> Cube:
    """
    cubic line drawing helper
    """
    return Cube(x=lerp(a.x, b.x, t), y=lerp(a.y, b.y, t), z=lerp(a.z, b.z, t))


def choice_from_dict(dictionary: dict) -> str:
    count = randint(1, sum(dictionary.values()))
    for key in dictionary.keys():
        count -= dictionary[key]
        if count <= 0:
            return key
