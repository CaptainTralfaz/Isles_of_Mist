from __future__ import annotations

from typing import Dict, List, TYPE_CHECKING

from actions.base import Action
from constants.colors import colors
from constants.enums import Location

if TYPE_CHECKING:
    from entity import Actor


class SplitDamageAction(Action):
    def __init__(self, entity: Actor,
                 targets: List[Actor],
                 damage: int,
                 direction: Location,
                 ammo: Dict[str, int]):
        """
        A split damage attack action divides total damage by number of targets hit
        :param entity: acting Entity
        :param targets: list of entities hit by the attack
        :param damage: total amount of damage done
        :param direction: the key pressed to make the attack
        :param ammo: dict of ammo:amount used for the attack
        """
        super().__init__(entity)
        self.targets = targets
        self.damage = damage
        self.direction = direction
        self.ammo = ammo
    
    def perform(self) -> bool:
        for target in self.targets:
            damage = self.damage - target.fighter.defense
            
            attack_desc = f"{self.entity.name.capitalize()} shoots {target.name}"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} for {damage} " +
                                                    f"{target.fighter.name} damage",
                                                    colors['mountain'])
                target.fighter.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage",
                                                    colors['mountain'])
        if self.direction == Location.PORT:
            for weapon in [w for w in self.entity.broadsides.port if w.cooldown == 0]:
                weapon.cooldown = weapon.cooldown_max
        elif self.direction == Location.STARBOARD:
            for weapon in [w for w in self.entity.broadsides.starboard if w.cooldown == 0]:
                weapon.cooldown = weapon.cooldown_max
        self.entity.cargo.remove_items_from_manifest(self.ammo)
        return True
