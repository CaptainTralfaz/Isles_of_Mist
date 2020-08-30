from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor


class Action:
    """Generic Action"""
    
    def __init__(self, entity: Actor):
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return engine for this action"""
        return self.entity.parent.engine

    def perform(self) -> bool:
        """Perform this action with the objects needed to determine its scope.
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


# class ActionEscape(Action):
#     def perform(self) -> None:
#         raise SystemExit()


class ActionQuit(Action):
    """Action that quits the game"""
    def perform(self) -> None:
        raise SystemExit()


class WaitAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
        self.entity = entity

    def perform(self) -> bool:
        print("{} waits...".format(self.entity.name))
        return True


class MovementAction(Action):
    def __init__(self, entity):
        super().__init__(entity)
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        """Return the engine for this action"""
        return self.entity.parent.engine
    
    def perform(self) -> bool:
        x, y = self.entity.get_next_hex()
        if self.entity.parent.in_bounds(x, y) and self.entity.parent.can_sail_to(x, y):
            self.entity.move()
            return True
        return False


class RotateAction(Action):
    def __init__(self, entity, direction):
        super().__init__(entity)
        self.entity = entity
        self.direction = direction
    
    @property
    def engine(self) -> Engine:
        """Return the engine for this action"""
        return self.entity.game_map.engine
    
    def perform(self) -> bool:
        self.entity.rotate(self.direction)
        return True
