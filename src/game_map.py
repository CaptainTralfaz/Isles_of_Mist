from pygame import display, image

from src.tile import Elevation, Terrain, tile_size


ocean = image.load("assets/ocean.png")
water = image.load("assets/water.png")
shallows = image.load("assets/shallows.png")
beach = image.load("assets/beach.png")
grass = image.load("assets/grass.png")
jungle = image.load("assets/jungle.png")
mountain = image.load("assets/mountain.png")
volcano = image.load("assets/volcano.png")


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
            self.terrain = [[Terrain(elevation=Elevation.OCEAN, explored=False) for y in range(height)] for x in range(width)]
        
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def can_sail_to(self, x: int, y: int) -> bool:
        return self.terrain[x][y].elevation < Elevation.BEACH
    
    def render(self, main_display: display) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if self.terrain[x][y].explored:
                    if self.terrain[x][y].elevation == Elevation.OCEAN:
                        tile = ocean
                    elif self.terrain[x][y].elevation == Elevation.WATER:
                        tile = water
                    elif self.terrain[x][y].elevation == Elevation.SHALLOWS:
                        tile = shallows
                    elif self.terrain[x][y].elevation == Elevation.BEACH:
                        tile = beach
                    elif self.terrain[x][y].elevation == Elevation.GRASS:
                        tile = grass
                    elif self.terrain[x][y].elevation == Elevation.JUNGLE:
                        tile = jungle
                    elif self.terrain[x][y].elevation == Elevation.MOUNTAIN:
                        tile = mountain
                    else:
                        tile = volcano
                    # TODO magic numbers
                    main_display.blit(tile, (x * tile_size - 10, y * tile_size + x % 2 * tile_size // 2 - 10 - 16))
