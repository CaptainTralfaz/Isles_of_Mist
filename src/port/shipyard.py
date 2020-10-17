class Shipyard:
    def __init__(self):
        self.temp_coins = 0
        self.upgrades = []
    
    def to_json(self):
        return {
            'upgrades': self.upgrades
        }
    
    @staticmethod
    def from_json(json_data):
        upgrades = json_data.get('upgrades')
        return upgrades


"""
Things to upgrade:

crew capacity   + 5 each    (8 available - up to 50)
hull points     + 5 each    (
sail points     + 2 each    ( up to 10 total per mast)
mast

cargo capacity  + 500 each  (6 available) - up to 4000
cargo weight    + 500 each  (6 available) - up to 4000

broadsides slots     + 1 each (3 available) - up to 4

view? No - this should come from "Spyglass" artifact (and eagle-eye crewman)... and 1 tall mast upgrade?
crew defense? No = comes from soldiers (max +1 defense, can have many soldiers though), plus another from artifact
hull defense? burn resist?
sail defense? burn resist?

artifacts:
spyglass:  +1 view
spiked hull: deal a damage to monsters on hit?
reinforced hull: -1 dmg from decorations

"""
