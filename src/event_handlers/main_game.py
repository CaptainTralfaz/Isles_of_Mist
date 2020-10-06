from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pygame import QUIT, KEYUP, KEYDOWN, KMOD_NONE, K_ESCAPE, MOUSEMOTION, mouse
from pygame import event as pygame_event

from action.attack.attack_choice import AttackAction
from action.auto.auto import AutoAction
from action.mouse import MouseMoveAction
from action.move.movement import MovementAction
from action.move.rotate import RotateAction
from action.port.port_choice import PortAction
from action.quit import ActionQuit
from action.repair.repair_choice import RepairAction
from action.ship_config.ship import ShipAction
from constants.colors import colors
from custom_exceptions import Impossible
from constants.enums import GameStates, KeyMod
from event_handlers.base import EventHandler
from constants.keys import MODIFIERS, ATTACK_KEYS, REPAIR_KEYS, PORT_KEYS, SHIP_KEYS, AUTO_KEYS, MOVEMENT_KEYS, ROTATE_KEYS

if TYPE_CHECKING:
    from engine import Engine
    from action.base import Action


class MainEventHandler(EventHandler):
    def __init__(self, engine: Engine):
        """
        handles keys and dispatches events for when player is dead
        :param engine: the game Engine
        """
        super().__init__(engine)
    
    def handle_events(self):
        something_happened = False
        # noinspection PyArgumentList
        events = pygame_event.get(pump=True)
        if len(events) > 0:
            for event in events:
                action = self.process_event(event)
                if action is None:
                    continue
                try:
                    something_happened = action.perform()
                
                except Impossible as e:
                    self.engine.message_log.add_message(e.args[0], colors['gray'])
                    return False
            
            if something_happened:
                self.engine.player.view.set_fov()
                if self.engine.player.broadsides:
                    self.engine.player.broadsides.tick_cooldown()
                self.engine.handle_bonus_movement()
                self.engine.handle_enemy_turns()
                self.engine.handle_weather()
                for entity in self.engine.game_map.entities:
                    if entity.is_alive:
                        entity.view.set_fov()
            if self.engine.game_state != GameStates.ACTION:
                self.engine.get_handler()
    
    def process_event(self, event) -> Optional[Action]:
        player = self.engine.player
        port = (player.x, player.y) == self.engine.game_map.port
        response = None
        if event.type == QUIT:
            response = ActionQuit(player)
        if event.type == KEYUP:
            if event.mod == KMOD_NONE:
                self.engine.key_mod = None
        if event.type == KEYDOWN:
            if event.mod in MODIFIERS:
                self.engine.key_mod = MODIFIERS[event.mod]
            if self.engine.key_mod == KeyMod.SHIFT and (event.key in ATTACK_KEYS or event.key in REPAIR_KEYS):
                if port:
                    response = RepairAction(player, REPAIR_KEYS[event.key])
                else:
                    response = AttackAction(player, ATTACK_KEYS[event.key])
            elif self.engine.key_mod == KeyMod.COMMAND and event.key in SHIP_KEYS:
                response = ShipAction(player, SHIP_KEYS[event.key], self.engine.game_state)
            elif port and self.engine.key_mod == KeyMod.OPTION and event.key in PORT_KEYS:
                response = PortAction(player, PORT_KEYS[event.key])
            if self.engine.key_mod is None:
                if event.key in ROTATE_KEYS:
                    response = RotateAction(player, ROTATE_KEYS[event.key])
                elif event.key in MOVEMENT_KEYS:
                    response = MovementAction(player)
                elif event.key in AUTO_KEYS:
                    response = AutoAction(player)
                elif event.key == K_ESCAPE:
                    response = ActionQuit(player)
        
        if event.type == MOUSEMOTION:
            response = MouseMoveAction(player, mouse.get_pos())
        
        if response is not None:
            return response