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

weapon_stats = {'ballista': {
    'weight': 20,
    'volume': 25,
    'category': 'weapon',
},
    'heavy ballista': {
        'weight': 30,
        'volume': 30,
        'category': 'weapon',
    },
    'repeating ballista': {
        'weight': 25,
        'volume': 30,
        'category': 'weapon',
    },
    'sniper ballista': {
        'weight': 25,
        'volume': 35,
        'category': 'weapon',
    },
    'cannon': {
        'weight': 30,
        'volume': 20,
        'category': 'weapon',
    },
    'heavy cannon': {
        'weight': 40,
        'volume': 25,
        'category': 'weapon',
    },
    'organ gun': {
        'weight': 35,
        'volume': 25,
        'category': 'weapon',
    },
    'long guns': {
        'weight': 35,
        'volume': 30,
        'category': 'weapon',
    },
}
