from __future__ import annotations

from typing import TYPE_CHECKING

from actions.attack.split_damage import SplitDamageAction
from constants.enums import Location
from custom_exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor


class ArrowAction(SplitDamageAction):
    def __init__(self, entity: Actor, direction: Location):
        """
        Arrow action hits all adjacent targets as well as entities at the attacker's location
        This is a split damage attack action that divides total damage by number of targets hit
        :param entity: acting Entity
        :param direction: key pressed to make attack
        """
        self.entity = entity
        ammo = {'arrows': self.entity.crew.count // 4}
        enough_ammo = True
        for ammo_type in ammo.keys():
            if ammo_type not in self.entity.cargo.manifest.keys():
                enough_ammo = False
            elif self.entity.cargo.manifest[ammo_type] - ammo[ammo_type] < 0:
                enough_ammo = False
        if not enough_ammo:
            raise Impossible(f"Not enough arrows!")
        
        targets = []
        neighbor_tiles = self.engine.game_map.get_neighbors_at_elevations(self.entity.x,
                                                                          self.entity.y,
                                                                          elevations='all')
        neighbor_tiles.append((entity.x, entity.y))
        for tile_x, tile_y in neighbor_tiles:
            targets.extend(self.engine.game_map.get_targets_at_location(tile_x, tile_y))
        if self.entity in targets:
            targets.remove(self.entity)
        if len(targets) < 1:
            raise Impossible(f"No adjacent targets")
        damage = (self.entity.crew.count // 4) // len(targets)
        super().__init__(entity, targets, damage, direction, ammo)
    
    def perform(self) -> bool:
        """
        perform a split damage attack
        :return: bool
        """
        return super().perform()
