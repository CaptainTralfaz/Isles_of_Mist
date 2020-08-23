from pygame import display, Surface

from src.tile import Elevation

tile_size = 32


class GameMap:
    def __init__(self, width, height, terrain=None):
        """
        The GameMap object, which holds the game map, map width, map height, tile information
        :param width: width of the game map
        :param height: height of the game map
        :param terrain: list of lists of Terrain tiles
        """
        self.width = width
        self.height = height
        
        if terrain:
            self.terrain = terrain
        else:
            self.terrain = [[0 for y in range(height)] for x in range(width)]
        
        self.terrain[10][10] = 5
        self.terrain[10][11] = 5
        self.terrain[11][11] = 5
    
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def can_sail_to(self, x: int, y: int) -> bool:
        return self.terrain[x][y] < Elevation.DUNES.value
    
    def render(self, main_display: display) -> None:
        block = Surface((tile_size, tile_size))
        block.fill((0, 150, 0))
        for x in range(self.width):
            for y in range(self.height):
                if self.terrain[x][y] > Elevation.DEEPS.value:
                    main_display.blit(block, (x * tile_size, y * tile_size + x % 2 * tile_size // 2))
