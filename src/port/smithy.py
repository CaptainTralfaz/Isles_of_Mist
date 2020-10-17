from random import randint
from typing import List

from components.weapon import Weapon
from constants.constants import SMITHY
from utilities import choice_from_dict


class Smithy:
    def __init__(self, manifest: List[Weapon] = None, coins: int = None):
        # TODO generate this depending on port's surroundings / buildings
        #  but for now...
        self.coins = coins if coins is not None else randint(50, 100)
        self.temp_coins = 0
        if manifest is not None:
            self.manifest = manifest
        else:
            self.manifest = []
            for x in range(0, randint(2, 3)):
                self.manifest.append(Weapon.make_weapon_from_name(choice_from_dict(SMITHY)))
    
    def to_json(self):
        return {'coins': self.coins,
                'manifest': [weapon.to_json() for weapon in self.manifest]}
    
    @staticmethod
    def from_json(json_data):
        manifest_data = json_data.get('manifest')
        manifest = []
        for weapon in manifest_data:
            manifest.append(Weapon.from_json(weapon))
        return Smithy(manifest=manifest, coins=json_data.get('coins'))
