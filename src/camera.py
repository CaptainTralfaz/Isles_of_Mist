from constants.constants import tile_size
from typing import Dict


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def to_json(self) -> Dict:
        return {
            'x': self.x,
            'y': self.y
        }
    
    def update(self, player):
        target_x = player.x * tile_size
        target_y = player.y * tile_size + ((player.x % 2) * tile_size // 2)

        distance_x = target_x - self.x
        distance_y = target_y - self.y
        
        x_step = 8
        if 0 < abs(distance_x) < x_step:      # if under 1 step
            self.x += distance_x // abs(distance_x)  # move by 1
        else:
            self.x += distance_x // x_step

        y_step = 8
        if 0 < abs(distance_y) < y_step:
            self.y += distance_y // abs(distance_y)
        else:
            self.y += distance_y // y_step

        # print(f"{distance_x}:{distance_y}")
