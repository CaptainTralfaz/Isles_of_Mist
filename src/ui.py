from render_functions import game_font, margin
from tile import tile_size

message_count = 8
block_size = 4
view_port = 8


class DisplayInfo:
    def __init__(self, map_width, map_height):
        self.mini_width = map_width * block_size + 2 * margin
        self.mini_height = map_height * block_size + 2 * margin - 2
        self.viewport_width = 2 * margin + (2 * view_port + 1) * tile_size - 10
        self.viewport_height = 2 * margin + (2 * view_port + 1) * tile_size
        self.status_width = self.mini_width
        self.messages_height = 2 * margin + message_count * game_font.get_height()
        self.display_width = self.mini_width + self.viewport_width
        self.display_height = self.viewport_height + self.messages_height
        self.status_height = self.display_height - self.mini_height
        self.messages_width = self.display_width - self.status_width
