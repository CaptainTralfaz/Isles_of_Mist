from enum import Enum
from constants import items
from entity import Entity
from components.base import BaseComponent


class Item:
    def __init__(self, name: str, quantity: int = 1):
        """
        Object holding an Item
        :param name: str name of the object
        # :param icon: str name for the icon of the object
        # :param category: category of the item     TODO: actually use this for sorting on the manifest display
        # :param weight: float weight of each individual item
        # :param volume: float volume of each individual item
        :param quantity: int number of items
        """
        self.name = name
        self.quantity = quantity
        # self.icon = icon


class Cargo(BaseComponent):
    parent: Entity
    
    def __init__(self, max_volume: float, max_weight: float, manifest=None):
        """
        Holds maximum weight and volume of a container, and a list of Items currently held
        TODO: make over-weight effect ship's damage taken from hitting decorations
        TODO: make over-volume items can be washed overboard in storm, or hit in combat
        :param max_volume: int maximum volume available in ship's cargo hold
        :param max_weight: int maximum weight a ship can SAFELY carry
        :param manifest: list of Items TODO: change this to a dict
        """
        self.max_volume = max_volume
        self.max_weight = max_weight
        self.manifest = {}
        if manifest:
            self.add_items_to_manifest(manifest)

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
        for item in self.manifest:
            weight += item.weight * item.quantity
        return weight
    
    @property
    def volume(self):
        """
        Determines total volume of cargo in manifest
        :return: total volume of cargo in manifest
        """
        volume = 0
        for item in self.manifest:
            volume += item.volume * item.quantity
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
            else:
                self.manifest[key] = item_dict[key]
        
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
#
#
# def adjust_quantity(cargo, item, amount, message_log):
#     """
#     Add or subtract quantity of an Item
#     :param cargo: cargo object
#     :param item: name of Item object
#     :param amount: amount to modify quantity by
#     :param message_log: game message log
#     :return: None - modify Item quantity directly
#     """
#     item.quantity += amount
#     if amount > 0:
#         message_log.add_message('{} {} added to cargo'.format(amount, item.name))
#     elif amount < 0 < amount + item.quantity:
#         message_log.add_message('{} {} removed from cargo'.format(abs(amount), item.name))
#     elif amount < 0 and (amount + item.quantity == 0):
#         message_log.add_message('All {} {} removed from cargo'.format(abs(amount), item.name))
#         cargo.remove_item_from_manifest(item=item, message_log=message_log)
#
#
# class ItemCategory(Enum):
#     """
#     Category type of item for sorting
#     """
#     MATERIALS = 0
#     GOODS = 1
#     EXOTICS = 3
#     SUPPLIES = 2
#     AMMO = 4
