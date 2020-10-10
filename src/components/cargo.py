from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from components.base import BaseComponent
from constants.stats import item_stats
from custom_exceptions import Impossible
from utilities import choice_from_dict

if TYPE_CHECKING:
    from entity import Entity


class Cargo(BaseComponent):
    parent: Entity
    
    def __init__(self, max_volume: float, max_weight: float, manifest: Dict = None, selected: int = 0):
        """
        Holds maximum weight and volume of a container, and a list of Items currently held
        :param max_volume: int maximum volume available in ship's cargo hold
        :param max_weight: int maximum weight a ship can SAFELY carry
        :param manifest: dict of item:quantity
        """
        self.max_volume = max_volume
        self.max_weight = max_weight
        self.manifest = manifest
        self.selected = selected
    
    def to_json(self):
        return {
            'max_volume': self.max_volume,
            'max_weight': self.max_weight,
            'manifest': self.manifest
        }
    
    @staticmethod
    def from_json(json_data):
        max_volume = json_data.get('max_volume')
        max_weight = json_data.get('max_weight')
        manifest = json_data.get('manifest')
        return Cargo(max_volume=max_volume, max_weight=max_weight, manifest=manifest)
    
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
                                                             text_color='beach')
            else:
                self.manifest[key] = item_dict[key]
                self.game_map.engine.message_log.add_message(f"Added {item_dict[key]} {key} to cargo",
                                                             text_color='beach')
    
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
                                                                     text_color='beach')
                        remove_key.append(key)
                        break
            else:
                raise Impossible(f"No such item {key} in manifest")
        if len(remove_key) > 0:
            for key in remove_key:
                del (self.manifest[key])
                
    def lose_random_cargo(self, count):
        total_losses = {}
        for loss in range(count):
            loss_choices = {}
            for key in self.manifest.keys():
                if item_stats[key]['volume'] > 1:
                    loss_choices[key] = self.manifest[key]
            loss_key = choice_from_dict(loss_choices)
            self.remove_items_from_manifest({str(loss_key): 1})
            if loss_key in total_losses:
                total_losses[loss_key] += 1
            else:
                total_losses[loss_key] = 1
        for loss in total_losses.keys():
            self.game_map.engine.message_log.add_message(f"{total_losses[loss]} {loss} was washed overboard!",
                                                         text_color='orange')
