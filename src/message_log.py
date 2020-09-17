import textwrap
from typing import Iterable, List, Reversible, Tuple

from pygame import Surface

from constants import colors
from render_functions import game_font, render_border
from ui import DisplayInfo
from constants import message_count, margin


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
    def __init__(self) -> None:
        self.messages: List[Message] = []
    
    def add_message(
            self, text: str, text_color: Tuple[int, int, int] = colors["white"], *, stack: bool = True,
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
        # TODO magic numbers
        message_surf = Surface((ui_layout.messages_width, ui_layout.messages_height))
        render_border(message_surf, colors['white'])
        self.render_messages(message_surf, 0, ui_layout.messages_height - 2 * margin,
                             ui_layout.messages_width - 2 * margin, message_count, self.messages)
        console.blit(message_surf, (ui_layout.status_width, ui_layout.viewport_height))
    
    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        """Return a wrapped text message."""
        for line in string.splitlines():  # Handle newlines in messages.
            yield from textwrap.wrap(line, width, expand_tabs=True)
    
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
            for line in reversed(list(cls.wrap(message.full_text, width))):
                message_surf.blit(game_font.render(f"{line}", True, message.color),
                                  (x + margin, y + margin - y_offset * game_font.get_height()))
                y_offset += 1
                if y_offset > height:
                    return message_surf
