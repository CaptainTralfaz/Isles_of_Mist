from actions.base.base import Action


class ActionQuit(Action):
    """Action that quits the game"""
    
    def perform(self) -> None:
        raise SystemExit()
