from typing import List, Reversible, Tuple

from pygame import Surface

from constants import colors, game_font, margin
from render_functions import render_border
from ui import DisplayInfo


class Message:
    def __init__(self, text: str, color: Tuple[int, int, int]):
        self.plain_text = text
        self.color = color
        self.count = 1


class MessageLog:
    def __init__(self, parent) -> None:
        self.messages: List[Message] = []
        self.parent = parent
    
    def add_message(
            self, text: str, text_color: Tuple[int, int, int] = colors['mountain'], *, stack: bool = True,
    ) -> None:
        """Add a message to this log.
        `text` is the message text, `fg` is the text color.
        If `stack` is True then the message can stack with a previous message
        of the same text.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, text_color))
    
    def render(self, console: Surface, ui_layout: DisplayInfo) -> None:
        """Render this log over the given area.
        `x`, `y`, `width`, `height` is the rectangular region to render onto
        the `console`.
        """
        message_surf = Surface((ui_layout.messages_width, ui_layout.messages_height))
        render_border(message_surf, self.parent.time.get_sky_color)
        self.render_messages(message_surf=message_surf, x=0, y=ui_layout.messages_height - 2 * margin,
                             height=(ui_layout.messages_height - 2 * margin) // game_font.get_height(),
                             messages=self.messages)
        console.blit(message_surf, (ui_layout.status_width, ui_layout.viewport_height))
    
    def render_max(self, console: Surface, ui_layout: DisplayInfo) -> None:
        """Render this log over the given area.
        `x`, `y`, `width`, `height` is the rectangular region to render onto
        the `console`.
        """
        message_surf = Surface((ui_layout.messages_width, ui_layout.display_height))
        render_border(message_surf, self.parent.time.get_sky_color)
        self.render_messages(message_surf=message_surf, x=0, y=ui_layout.display_height - 2 * margin,
                             height=(ui_layout.display_height - 2 * margin) // game_font.get_height(),
                             messages=self.messages)
        console.blit(message_surf, (ui_layout.status_width, 0))
    
    @classmethod
    def render_messages(
            cls,
            message_surf: Surface,
            x: int,
            y: int,
            height: int,  # height in messages
            messages: Reversible[Message],
    ) -> Surface:
        """Render the messages provided.
        The `messages` are rendered starting at the last message and working
        backwards.
        """
        y_offset = 1
        
        for message in reversed(messages):
            count = ""
            if message.count > 1:
                count = f" (x {message.count})"
            text = f"{message.plain_text}{count}"
            message_surf.blit(game_font.render(text, True, message.color),
                              (x + margin, y + margin - y_offset * game_font.get_height()))
            y_offset += 1
            if y_offset > height:
                return message_surf
