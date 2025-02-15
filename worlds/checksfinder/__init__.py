import os
import json
from base64 import b64encode, b64decode
from math import ceil

from .Items import ChecksFinderItem, item_table, required_items
from .Locations import ChecksFinderAdvancement, advancement_table, exclusion_table
from .Regions import checksfinder_regions, link_checksfinder_structures
from .Rules import set_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item, Tutorial
from .Options import checksfinder_options
from ..AutoWorld import World, WebWorld

client_version = 7


class ChecksFinderWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago ChecksFinder software on your computer. This guide covers "
        "single-player, multiworld, and related software.",
        "English",
        "checksfinder_en.md",
        "checksfinder/en",
        ["Mewlif"]
    )]


class ChecksFinderWorld(World):
    """
    ChecksFinder is a game where you avoid mines and find checks inside the board
    with the mines! You win when you get all your items and beat the board!
    """
    game: str = "ChecksFinder"
    options = checksfinder_options
    topology_present = True
    web = ChecksFinderWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 4

    def _get_checksfinder_data(self):
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'race': self.world.is_race,
        }

    def generate_basic(self):

        # Generate item pool
        itempool = []
        # Add all required progression items
        for (name, num) in required_items.items():
            itempool += [name] * num
        # Add the map width and height stuff
        itempool += ["Map Width"] * (10-5)
        itempool += ["Map Height"] * (10-5)
        # Add the map bombs
        itempool += ["Map Bombs"] * (20-5)
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()

        self.world.itempool += itempool

    def set_rules(self):
        set_rules(self.world, self.player)
        set_completion_rules(self.world, self.player)

    def create_regions(self):
        def ChecksFinderRegion(region_name: str, exits=[]):
            ret = Region(region_name, None, region_name, self.player, self.world)
            ret.locations = [ChecksFinderAdvancement(self.player, loc_name, loc_data.id, ret)
                for loc_name, loc_data in advancement_table.items()
                if loc_data.region == region_name]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.world.regions += [ChecksFinderRegion(*r) for r in checksfinder_regions]
        link_checksfinder_structures(self.world, self.player)

    def fill_slot_data(self):
        slot_data = self._get_checksfinder_data()
        for option_name in checksfinder_options:
            option = getattr(self.world, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = ChecksFinderItem(name, item_data.progression, item_data.code, self.player)
        return item
