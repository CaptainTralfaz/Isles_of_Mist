class Action:
    pass


class EscapeAction(Action):
    pass


class MovementAction(Action):
    def __init__(self, direction: int):
        super().__init__()

        self.direction = direction


class RotateAction(Action):
    def __init__(self, rotate: int):
        super().__init__()
        self.rotate = rotate


class ActionQuit(Action):
    """Action that quits the game"""

    def __init__(self):
        """Space intentionally left blank"""
        pass

    def perform(self) -> None:
        raise SystemExit()
