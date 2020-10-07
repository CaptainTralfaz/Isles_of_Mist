from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from actions.base import Action
from constants.colors import colors
from utilities import choice_from_dict

if TYPE_CHECKING:
    from entity import Actor


class MeleeAction(Action):
    def __init__(self, entity: Actor):
        """
        Melee action hits a single target (typically the player)
        :param entity: acting Entity
        """
        super().__init__(entity)
    
    @property
    def target(self) -> Optional[Actor]:
        return self.engine.player
    
    def perform(self) -> bool:
        
        if "sail" in self.entity.fighter.can_hit.keys() and ((not self.target.sails)
                                                             or self.target.sails.hp == 0
                                                             or (not self.target.sails.raised)):
            self.entity.fighter.can_hit["sail"] = 0
        
        if "weapon" in self.entity.fighter.can_hit.keys() and ((not self.target.broadsides)
                                                               or (len(self.target.broadsides.port)
                                                                   + len(self.target.broadsides.starboard) < 1)):
            self.entity.fighter.can_hit["weapon"] = 0
        
        gets_hit = choice_from_dict(self.entity.fighter.can_hit)
        
        if gets_hit == "hull":
            damage = self.entity.fighter.power - self.target.fighter.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.fighter.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} damage", colors['pink'])
                self.target.fighter.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors['pink'])
        elif gets_hit == "sail":
            damage = self.entity.fighter.power - self.target.sails.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.sails.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} damage", colors['pink'])
                self.target.sails.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors['pink'])
        elif gets_hit == "crew":
            damage = self.entity.fighter.power - self.target.crew.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {self.target.crew.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} and kills {damage} members", colors['pink'])
                self.target.crew.take_damage(damage)
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors['pink'])
        elif gets_hit == "weapon":
            weapon, location = self.target.broadsides.pick_weapon()
            damage = self.entity.fighter.power - weapon.defense
            attack_desc = f"{self.entity.name.capitalize()} attacks {self.target.name}'s {weapon.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} damage", colors['pink'])
                destroy = weapon.hp - damage
                if destroy <= 0:
                    self.engine.message_log.add_message(
                        f"{location.name.capitalize()} {weapon.name.capitalize()} was destroyed!", colors['orange'])
                weapon.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage", colors['pink'])
        return True
