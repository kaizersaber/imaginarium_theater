from logic.season import Season
from datetime import datetime


def test_init():
    test_season = Season("202502")

    assert test_season.date == datetime(2025, 2, 1).date()

    expected_alt_cast_elements = ["Pyro", "Hydro", "Anemo"]

    assert test_season.alt_cast_elements == expected_alt_cast_elements

    expected_op_characters = [
        "Hu Tao",
        "Gaming",
        "Mona",
        "Xingqiu",
        "Venti",
        "Shikanoin Heizou",
    ]

    assert test_season.op_characters == expected_op_characters

    expected_special_invites = ["Keqing", "Ororon", "Citlali", "Yun Jin"]

    assert test_season.special_invites == expected_special_invites


def test_count_elig_characters():
    test_season = Season("202501")

    test_character_inventory = []
    assert test_season.count_elig_characters_in(test_character_inventory) == 6

    test_character_inventory = test_season.op_characters
    assert test_season.count_elig_characters_in(test_character_inventory) == 6

    test_character_inventory = ["Traveler"]
    assert test_season.count_elig_characters_in(test_character_inventory) == 7

    test_character_inventory = test_season.special_invites
    assert test_season.count_elig_characters_in(test_character_inventory) == 10

    test_character_inventory = [
        "Xiangling",
        "Jean",
        "Diona",
        "Kachina",
        "Keqing",
        "Tighnari",
        "Barbara",
    ]
    assert test_season.count_elig_characters_in(test_character_inventory) == 9
