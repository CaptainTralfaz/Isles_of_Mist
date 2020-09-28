from constants import tile_size


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def update(self, player, ui):
        target_x = player.x * tile_size + tile_size // 2 + 5
        target_y = player.y * tile_size + tile_size // 2 - 5

        distance_x = target_x - self.x
        distance_y = target_y - self.y
        
        self.x += int(distance_x * .1)
        self.y += int(distance_y * .1)
