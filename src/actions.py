from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine import Engine
    from src.entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.
        `engine` is the scope this action is being performed in.
        `entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, direction: int):
        super().__init__()

        self.direction = direction

    def perform(self, engine: Engine, entity: Entity) -> None:
        x, y = entity.get_next_hex()
        if engine.game_map.can_sail_to(x, y):
            entity.move()


class RotateAction(Action):
    def __init__(self, rotate: int):
        super().__init__()
        self.rotate = rotate

    def perform(self, engine: Engine, entity: Entity) -> None:
        direction = self.rotate
        entity.rotate(direction)


class ActionQuit(Action):
    """Action that quits the game"""

    def __init__(self):
        """Space intentionally left blank"""
        pass

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()
