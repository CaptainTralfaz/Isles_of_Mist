from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base import Action
from constants.colors import colors
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor


class MovementAction(Action):
    def __init__(self, entity: Actor):
        """
        attempts to move the entity forward 1 hex in the direction it is facing
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    def perform(self) -> bool:
        x, y = self.entity.get_next_hex()
        if self.entity.game_map.in_bounds(x, y):
            # TODO currently no decorations on land (except port)
            # use this for when a point of interest is added to a coastline space,
            #  examples: hermit hut, fisherman village, "X" marks the spot
            # event = (self.entity == self.engine.player and
            #          self.entity.game_map.terrain[x][y].decoration is not None)
            can_move = (self.entity.game_map.can_move_to(x, y, self.entity.elevations)
                        and not (x, y) == self.engine.game_map.port.location) \
                       or ((x, y) == self.engine.game_map.port.location and self.entity == self.engine.player)
            if can_move:
                self.entity.move()
                if (x, y) == self.engine.game_map.port.location and self.entity is self.engine.player:
                    self.engine.message_log.add_message(f"Welcome to {self.engine.game_map.port.name}!",
                                                        colors['cyan'])
                    if self.entity.sails.raised:
                        self.entity.sails.adjust()
                # damage from terrain decorations
                elif self.entity.game_map.terrain[x][y].decoration is not None:
                    self.entity.game_map.decoration_damage(x=x, y=y, entity=self.entity,
                                                           conditions=self.engine.weather.conditions)
                return True
            # player can't move here
            elif self.entity == self.engine.player:
                if self.entity.sails and self.entity.sails.hp > 0 and self.entity.sails.raised:
                    self.engine.message_log.add_message("Blocked", colors['gray'])
                    self.entity.sails.adjust()
                else:
                    raise Impossible("Blocked")
            return False
        # player out of bounds
        elif self.entity == self.engine.player:
            if self.entity.sails and self.entity.sails.hp > 0 and self.entity.sails.raised:
                self.engine.message_log.add_message("No Navigational Charts to leave area", colors['gray'])
                self.entity.sails.adjust()
            else:
                raise Impossible("No Navigational Charts to leave area")
