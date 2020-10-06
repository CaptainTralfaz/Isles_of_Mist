from typing import Dict

from components.base import BaseComponent
from constants.colors import colors
from constants.stats import item_stats
from custom_exceptions import Impossible
from entity import Entity


class Cargo(BaseComponent):
    parent: Entity
    
    def __init__(self, max_volume: float, max_weight: float, manifest: Dict = None, selected: int = 0):
        """
        Holds maximum weight and volume of a container, and a list of Items currently held
        TODO: make over-weight effect ship's damage taken from hitting decorations
        TODO: make over-volume items can be washed overboard in storm, or hit in combat
        :param max_volume: int maximum volume available in ship's cargo hold
        :param max_weight: int maximum weight a ship can SAFELY carry
        :param manifest: dict of item:quantity
        """
        self.max_volume = max_volume
        self.max_weight = max_weight
        self.manifest = manifest
        self.selected = selected
    
    # def to_json(self):
    #     return {
    #         'max_volume': self.max_volume,
    #         'max_weight': self.max_weight,
    #         'manifest': [item.to_json() for item in self.manifest]
    #     }
    
    # @staticmethod
    # def from_json(json_data):
    #     max_volume = json_data.get('max_volume')
    #     max_weight = json_data.get('max_weight')
    #     manifest = [Item.from_json(item) for item in json_data.get('manifest')]
    #
    #     return Cargo(max_volume=max_volume, max_weight=max_weight, manifest=manifest)
    
    @property
    def weight(self):
        """
        Determines total weight of cargo in manifest
        :return: total weight of cargo in manifest
        """
        weight = 0
        for item in self.manifest.keys():
            weight += item_stats[item]['weight'] * self.manifest[item]
        return weight
    
    @property
    def volume(self):
        """
        Determines total volume of cargo in manifest
        :return: total volume of cargo in manifest
        """
        volume = 0
        for item in self.manifest.keys():
            volume += item_stats[item]['volume'] * self.manifest[item]
        return volume
    
    def add_items_to_manifest(self, item_dict: dict):
        """
        Add a new item:count to the manifest, or increase existing count
        :param item_dict: dict of (items: quantity) to be added
        :return: None - modifies manifest directly
        """
        for key in item_dict.keys():
            if key in self.manifest.keys():
                self.manifest[key] += item_dict[key]
                self.game_map.engine.message_log.add_message(f"Added {item_dict[key]} {key} to cargo",
                                                             colors['beach'])
            else:
                self.manifest[key] = item_dict[key]
                self.game_map.engine.message_log.add_message(f"Added {item_dict[key]} {key} to cargo",
                                                             colors['beach'])
    
    def item_type_in_manifest(self, key: str) -> bool:
        """
        returns true if the item is in the manifest, and the quantity is one or more
        :param key: str name of item
        :return: bool
        """
        return bool(key in self.manifest.keys() and self.manifest[key] > 0)
    
    def remove_items_from_manifest(self, item_dict: dict):
        """
        Removes an item from the manifest
        :param item_dict: dict of (items: quantity) to be added
        :return: None - modifies manifest directly
        """
        remove_key = []
        for key in item_dict.keys():
            if key in self.manifest.keys():
                for qty in range(item_dict[key]):
                    self.manifest[key] -= 1
                    if self.manifest[key] < 1:
                        self.game_map.engine.message_log.add_message(f"Removed all {key} from cargo",
                                                                     colors['beach'])
                        remove_key.append(key)
                        break
                
                # if not item_stats[key]['category'] == 'ammo':
                #     self.game_map.engine.message_log.add_message(f"Removed {item_dict[key]} {key} from cargo",
                #                                                  colors['beach'])
                #     self.game_map.engine.message_log.add_message(f"{self.manifest[key]} {key} left in cargo",
                #                                                  colors['beach'])
            else:
                raise Impossible(f"No such item {key} in manifest")
        if len(remove_key) > 0:
            for key in remove_key:
                del (self.manifest[key])
