from components.base import BaseComponent
from constants import colors
from constants import item_stats
from entity import Entity


class Cargo(BaseComponent):
    parent: Entity
    
    def __init__(self, max_volume: float, max_weight: float, manifest=None):
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
        Add a new item to the manifest
        :param item_dict: dict of (items: quantity) to be added
        # :param message_log: game message log
        :return: None - modifies manifest directly
        """
        for key in item_dict.keys():
            if key in self.manifest.keys():
                self.manifest[key] += item_dict[key]
                self.game_map.engine.message_log.add_message(f"Added {item_dict[key]} {key} to cargo", colors['beach'])
            else:
                self.manifest[key] = item_dict[key]
                self.game_map.engine.message_log.add_message(f"Added {item_dict[key]} {key} to cargo", colors['beach'])
        print(self.weight)
        print(self.volume)
    # def remove_item_from_manifest(self, item, message_log):
    #     """
    #     Removes an item from the manifest
    #     :param item: Item object to be removed
    #     :param message_log: game message log
    #     :return: None - modifies manifest directly
    #     """
    #     if item in self.manifest:
    #         self.manifest.remove(item)
    #         message_log.add_message(message="removed {} from manifest".format(item.name))
    #     else:
    #         message_log.add_message(message="not carrying any {}".format(item.name))

#     def to_json(self):
#         """
#         Serialize Item object to json
#         :return: json representation of Item object
#         """
#         return {
#             'name': self.name,
#             'quantity': self.quantity
#         }
#
#     @staticmethod
#     def from_json(json_data):
#         """
#         Deserialize Item object from json
#         :param json_data: json representation of Item object
#         :return: Item Object
#         """
#         name = json_data.get('name')
#         weight = json_data.get('weight')
#         volume = json_data.get('volume')
#         quantity = json_data.get('quantity')
#         icon = json_data.get('icon')
#         category = json_data.get('category')
#
#         return Item(name=name, quantity=quantity)
#
#     def get_item_weight(self):
#         """
#         Determines the total weight of an Item
#         :return: float total weight of Item
#         """
#         return self.weight * self.quantity
#
#     def get_item_volume(self):
#         """
#         Determines the total volume of an Item
#         :return: float total volume of Item
#         """
#         return self.volume * self.quantity
