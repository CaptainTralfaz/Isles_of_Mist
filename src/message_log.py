from typing import List, Reversible, Tuple

from pygame import Surface

from constants import colors, game_font
from constants import message_count, margin
from render_functions import render_border
from ui import DisplayInfo


class Message:
    def __init__(self, text: str, color: Tuple[int, int, int]):
        self.plain_text = text
        self.color = color
        self.count = 1
    
    @property
    def full_text(self) -> str:
        """The full text of this message, including the count if necessary."""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


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
        self.render_messages(message_surf, 0, ui_layout.messages_height - 2 * margin,
                             ui_layout.messages_width - 2 * margin, message_count, self.messages)
        console.blit(message_surf, (ui_layout.status_width, ui_layout.viewport_height))
    
    @classmethod
    def render_messages(
            cls,
            message_surf: Surface,
            x: int,
            y: int,
            width: int,
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
