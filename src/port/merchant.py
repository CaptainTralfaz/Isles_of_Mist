from random import randint
from typing import Dict

from constants.constants import MERCHANT
from utilities import choice_from_dict


class Merchant:
    def __init__(self, manifest: Dict = None, coins: int = None):
        self.coins = coins if coins is not None else randint(200, 300)
        self.temp_coins = 0
        # TODO generate this depending on port's surroundings / buildings
        #  but for now...
        if manifest is not None:
            self.manifest = manifest
        else:
            self.manifest = {}
            for x in range(0, randint(100, 200)):
                pick = choice_from_dict(MERCHANT)
                if pick in self.manifest.keys():
                    self.manifest[pick] += 1
                else:
                    self.manifest[pick] = 1
    
    def to_json(self):
        return {'coins': self.coins,
                'manifest': self.manifest}
    
    @staticmethod
    def from_json(json_data):
        return Merchant(manifest=json_data.get('manifest'), coins=json_data.get('coins'))
