from typing import Dict
from BaseClasses import MultiWorld
from Options import Choice, Option


class GameDifficulty(Choice):
    """The difficulty of the campaign, affects enemy AI, starting units, and game speed."""
    display_name = "Game Difficulty"
    option_casual = 0
    option_normal = 1
    option_hard = 2
    option_brutal = 3


class UpgradeBonus(Choice):
    """Determines what lab upgrade to use, whether it is Ultra-Capacitors which boost attack speed with every weapon upgrade
    or Vanadium Plating which boosts life with every armor upgrade."""
    display_name = "Upgrade Bonus"
    option_ultra_capacitors = 0
    option_vanadium_plating = 1


class BunkerUpgrade(Choice):
    """Determines what bunker lab upgrade to use, whether it is Shrike Turret which outfits bunkers with an automated turret or
    Fortified Bunker which boosts the life of bunkers."""
    display_name = "Bunker Upgrade"
    option_shrike_turret = 0
    option_fortified_bunker = 1


class AllInMap(Choice):
    """Determines what version of All-In (final map) that will be generated for the campaign."""
    display_name = "All In Map"
    option_ground = 0
    option_air = 1


# noinspection PyTypeChecker
sc2wol_options: Dict[str, Option] = {
    "game_difficulty": GameDifficulty,
    "upgrade_bonus": UpgradeBonus,
    "bunker_upgrade": BunkerUpgrade,
    "all_in_map": AllInMap,
}


def get_option_value(world: MultiWorld, player: int, name: str) -> int:
    option = getattr(world, name, None)

    if option == None:
        return 0

    return int(option[player].value)
