class Sprite:
    def __init__(self, sprite_name: str, sprite_count: int, flicker_timer: float, animation_speed: float):
        self.sprite_name = sprite_name
        self.pointer = 0
        self.sprite_count = sprite_count
        self.flicker_timer = flicker_timer
        self.flicker_speed = animation_speed / sprite_count
    
    def update(self, fps):
        if fps > 0.0:
            self.flicker_timer += 1 / fps
        if self.flicker_timer >= self.flicker_speed:
            self.flicker_timer = 0
            self.pointer += 1
        if self.pointer >= self.sprite_count:
            self.pointer = 0
