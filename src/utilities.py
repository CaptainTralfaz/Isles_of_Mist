from typing import Tuple

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
                   Cube(-1, 1, 0)   # (5) upper left
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


def cube_add(cube1, cube2):
    """
    adds the cubic coordinate values of two cubes
    :param cube1: first cube
    :param cube2: second cube
    :return: cubic coordinates
    """
    return Cube(x=cube1.x + cube2.x, y=cube1.y + cube2.y, z=cube1.z + cube2.z)


def cube_direction(direction):
    """
    Returns neighboring cubic relational values in a given hex direction
    :param direction: int direction
    :return: cubic relational values of neighbor in given hex direction
    """
    return cube_directions[direction]


def cube_neighbor(cube, direction):
    """
    Returns neighboring cubic coordinates in a given hex direction
    :param cube: cubic coordinates
    :param direction: int direction
    :return: cubic coordinates of neighbor in the given direction
    """
    return cube_add(cube1=cube, cube2=cube_direction(direction))


def move_entity(old_x: int, old_y: int, direction: int) -> Tuple[int, int]:
    old_cube = hex_to_cube(Hex(old_x // 32, old_y // 32))
    print("old cube: {}, {}, {}".format(old_cube.x, old_cube.y, old_cube.z))
    
    target_cube = cube_neighbor(old_cube, direction)
    print("target cube: {}, {}, {}".format(target_cube.x, target_cube.y, target_cube.z))
    
    new_hex = cube_to_hex(target_cube)
    print(new_hex.col, new_hex.row)
    return new_hex.col * 32, new_hex.row * 32
