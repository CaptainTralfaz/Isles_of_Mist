from constants.constants import message_count, block_size, view_port, tile_size, game_font, margin


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
        self.messages_width = self.display_width - self.status_width
        self.control_height = self.messages_height
        self.control_width = self.mini_width
        self.status_height = self.display_height - self.mini_height - self.control_height
    
    def in_viewport(self, x: int, y: int) -> bool:
        return self.mini_width <= x < self.display_width - 1 and 0 < y < self.viewport_height - 1
    
    def in_messages(self, x: int, y: int) -> bool:
        return self.mini_width <= x < self.display_width - 1 and \
               self.viewport_height + (self.messages_height // 2) < y < self.display_height - 1
