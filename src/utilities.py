from random import randint, choice
from typing import List, Tuple, Dict

from constants.enums import Location

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
    def __init__(self, column: int, row: int) -> None:
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
    """
    convenience function to get the next hex in a direction
    :param x: int x in map grid
    :param y: int x in map grid
    :param direction: direction to get next hex
    :return: return new coordinates
    """
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


def cube_rotate_clockwise(cube) -> Cube:
    """
    Returns cubic coordinates of a tile when rotated clockwise one direction
    :param cube: cube coords to rotate
    :return: rotated coordinates
    """
    new_x = - cube.y
    new_y = - cube.z
    new_z = - cube.x
    return Cube(x=new_x, y=new_y, z=new_z)


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


def choice_from_dict(dictionary: Dict[str, int]) -> str:
    """
    chooses a key from a dictionary of weighted values
    :param dictionary: dictionary of weighted values
    :return: name of the key chosen
    """
    count = randint(1, sum(dictionary.values()))
    for key in dictionary.keys():
        count -= dictionary[key]
        if count <= 0:
            return key


def reverse_direction(direction: int) -> int:
    """
    Returns value of the opposite direction
    :param direction: int current direction
    :return: int opposite direction
    """
    new_direction = direction - 3
    if new_direction < 0:
        return new_direction + 6
    else:
        return new_direction


def get_cone_target_hexes_at_location(entity_x: int,
                                      entity_y: int,
                                      facing: int,
                                      location: Location,
                                      max_range: int) -> List[Tuple[int, int]]:
    """
    Returns list of tile coordinates that can be targeted from a given facing the weapon list
    :param entity_x: int attacking entity x coordinate
    :param entity_y: int attacking entity y coordinate
    :param facing: int attacking entity facing
    :param location: Enum port or Starboard
    :param max_range: int distance the weapon can shoot
    :return: list of tile coordinates
    """
    target_hexes = []
    p_cube = hex_to_cube(hexagon=Hex(column=entity_x, row=entity_y))
    if location == Location.PORT:
        target_hexes.extend(get_cone_target_cubes(max_range=max_range,
                                                  p_cube=p_cube,
                                                  p_direction=facing))
    if location == Location.STARBOARD:
        target_hexes.extend(get_cone_target_cubes(max_range=max_range,
                                                  p_cube=p_cube,
                                                  p_direction=reverse_direction(direction=facing)))
    return target_hexes


def get_cone_target_cubes(max_range: int, p_cube: Cube, p_direction: int) -> List[Tuple[int, int]]:
    """
    Returns a list of tile coordinates between a given direction's two axes
    :param max_range: int maximum distance a weapon can shoot
    :param p_cube: cubic coordinates of attacker
    :param p_direction: int attacker's facing
    :return: list of tile coordinates
    """
    # this assumes direction 0, location x0 y0 z0
    target_cubes = []
    for x in range(1, max_range + 1):
        for y in range(0, x + 1):
            target_cubes.append(Cube(x=-x, y=y, z=x - y))
    # rotate and translate, then convert to (x, y)
    target_hexes = []
    for cube in target_cubes:
        r_cube = cube
        for step in range(6 - p_direction):
            r_cube = cube_rotate_clockwise(cube=r_cube)
        t_cube = cube_add(cube1=p_cube, cube2=r_cube)
        t_hex = cube_to_hex(cube=t_cube)
        target_hexes.append((t_hex.col, t_hex.row))
    return target_hexes


def closest_rotation(target: Tuple[int, int], entity_x: int, entity_y: int, direction: int) -> int:
    """
    Chooses shortest rotation distance of two adjacent hexes depending on entity direction
    :param target: x, y coordinates of hex
    :param entity_x: int x value of entity location
    :param entity_y: int y value of entity location
    :param direction: int direction entity is facing
    :return: direction to rotate
    """
    facing_left = direction
    for turns in range(0, 5):
        facing_left -= 1
        if facing_left < 0:
            facing_left = 5
        left_hex = get_neighbor(entity_x, entity_y, facing_left)
        if left_hex == target:
            if turns in [0, 1]:  # left is shorter
                return -1
            elif turns in [3, 4]:  # right is shorter
                return 1
            else:  # 2: directly behind - turn randomly
                return choice([-1, 1])


def remove_zero_quantities(manifest: Dict) -> Dict:
    del_list = []
    for key in manifest.keys():
        if manifest[key] == 0 and key != "arrows":
            del_list.append(key)
    for key in del_list:
        del (manifest[key])
    return manifest
    
