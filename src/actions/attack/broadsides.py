from __future__ import annotations

from typing import TYPE_CHECKING

from actions.attack.split_damage import SplitDamageAction
from custom_exceptions import Impossible
from constants.enums import Location
from utilities import get_cone_target_hexes_at_location

if TYPE_CHECKING:
    from entity import Actor


class BroadsideAction(SplitDamageAction):
    def __init__(self, entity: Actor, direction: Location):
        """
        Broadside action hits all targets in a cone in a particular side direction up to a certain range
        This is a split damage attack action that divides total damage by number of targets hit
        :param entity: acting Entity
        :param direction: key pressed to make attack
        """
        self.entity = entity
        
        distance = self.entity.broadsides.get_active_range(direction)
        if distance:
            damage = self.entity.broadsides.get_active_power(direction)
        else:
            raise Impossible(f"No active weapons to {direction.name.lower().capitalize()}")
        ammo = self.entity.broadsides.get_active_weapon_ammo_types(direction)
        enough_ammo = True
        for ammo_type in ammo.keys():
            if ammo_type not in self.entity.cargo.manifest.keys():
                enough_ammo = False
            elif self.entity.cargo.manifest[ammo_type] - ammo[ammo_type] < 0:
                enough_ammo = False
        if not enough_ammo:
            raise Impossible(f"Not enough ammo to fire {direction.name.lower().capitalize()} Broadsides")
        targets = []
        hexes = get_cone_target_hexes_at_location(entity.x, entity.y, entity.facing, direction, distance)
        for x, y in hexes:
            if (x, y) in entity.view.fov:
                targets.extend(self.engine.game_map.get_targets_at_location(x, y))
        if self.entity in targets:
            targets.remove(self.entity)
        if len(targets) < 1:
            raise Impossible(f"No targets to {direction.name.lower().capitalize()}")
        
        damage = damage // len(targets)
        super().__init__(entity, targets, damage, direction, ammo)
    
    def perform(self) -> bool:
        return super().perform()
