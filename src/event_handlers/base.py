from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from engine import Engine
    
    
class EventHandler:
    def __init__(self, engine: Engine):
        self.engine = engine
    
    def handle_events(self):
        raise NotImplementedError()
