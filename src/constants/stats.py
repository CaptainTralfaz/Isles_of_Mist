from yaml import load, Loader

from constants.enums import ItemType


def get_items():
    data = None
    with open(file="data/items.yaml", mode="r") as stream:
        try:
            data = load(stream, Loader=Loader)
        except FileNotFoundError:
            print(f"loading error on {stream}")
        for item in data['item_stats'].keys():
            data['item_stats'][item]['category'] = ItemType(data['item_stats'][item]['category'])
    
    return data['item_stats']


item_stats = get_items()


def get_occupations():
    data = None
    with open(file="data/occupations.yaml", mode="r") as stream:
        try:
            data = load(stream, Loader=Loader)
        except FileNotFoundError:
            print(f"loading error on {stream}")
    
    return data['occupations']


occupation_stats = get_occupations()
