from __future__ import annotations
from typing import Dict


class Sprite:
    def __init__(self, sprite_name: str, sprite_count: int, flicker_timer: float, animation_speed: float = None,
                 pointer: int = None, flicker_speed: float = None):
        self.sprite_name = sprite_name
        self.pointer = 0 if pointer is None else pointer
        self.sprite_count = sprite_count
        self.flicker_timer = flicker_timer
        self.flicker_speed = animation_speed / sprite_count if flicker_speed is None else flicker_speed
    
    def to_json(self) -> Dict:
        return {
            'sprite_name': self.sprite_name,
            'pointer': self.pointer,
            'sprite_count': self.sprite_count,
            'flicker_timer': self.flicker_timer,
            'flicker_speed': self.flicker_speed
        }
    
    @staticmethod
    def from_json(json_data: Dict) -> Sprite:
        sprite_name = json_data.get('sprite_name')
        pointer = json_data.get('pointer')
        sprite_count = json_data.get('sprite_count')
        flicker_timer = json_data.get('flicker_timer')
        flicker_speed = json_data.get('flicker_speed')
        return Sprite(sprite_name, sprite_count, flicker_timer, pointer=pointer, flicker_speed=flicker_speed)
    
    def update(self, fps: int) -> None:
        """
        update sprite time counter - change picture if necessary
        :param fps: frames per second
        :return: None
        """
        if fps > 0.0:
            self.flicker_timer += 1 / fps
        if self.flicker_timer >= self.flicker_speed:
            self.flicker_timer = 0
            self.pointer += 1
        if self.pointer >= self.sprite_count:
            self.pointer = 0
