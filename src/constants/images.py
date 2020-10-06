from pygame import image
from yaml import load, Loader


def get_images():
    data = None
    with open(file="data/images.yaml", mode="r") as stream:
        try:
            data = load(stream, Loader=Loader)
        except FileNotFoundError:
            print(f"loading error on {stream}")
        entities = {}
        terrain = {}
        cargo = {}
        misc = {}
        image_dicts = {
            'entities': entities,
            'terrain': terrain,
            'cargo': cargo,
            'misc': misc,
        }
        for key in data['assets'].keys():
            for sprite in data['assets'][key]:
                icon = image.load(f"assets/{key}/{sprite}.png")
                image_dicts[key][sprite] = icon
        _entity_icons = image_dicts['entities']
        _terrain_icons = image_dicts['terrain']
        _cargo_icons = image_dicts['cargo']
        _misc_icons = image_dicts['misc']
    
    return _entity_icons, _terrain_icons, _cargo_icons, _misc_icons


entity_icons, terrain_icons, cargo_icons, misc_icons = get_images()
