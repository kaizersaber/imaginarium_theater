from datetime import datetime
from season import Season


def test_init():
    test_season = Season("February 2025")
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

    expected_special_invites = ["Clorinde", "Ororon", "Citlali", "Yun Jin"]
    assert test_season.special_invites == expected_special_invites


def test_get_elig_char_breakdown_in():
    test_season = Season("January 2025")

    test_inventory = []
    assert test_season.get_elig_char_breakdown_in(test_inventory).n_chars() == 6

    test_inventory = test_season.op_characters
    assert test_season.get_elig_char_breakdown_in(test_inventory).n_chars() == 6

    test_inventory = ["Traveler"]
    assert test_season.get_elig_char_breakdown_in(test_inventory).n_chars() == 7

    test_inventory = test_season.special_invites
    assert test_season.get_elig_char_breakdown_in(test_inventory).n_chars() == 10

    test_inventory = [
        "Xiangling",
        "Jean",
        "Diona",
        "Kachina",
        "Keqing",
        "Tighnari",
        "Barbara",
    ]
    assert test_season.get_elig_char_breakdown_in(test_inventory).n_chars() == 9


def test_highest_tier():
    test_counts = [6, 8, 10, 12, 14, 16, 18, 22]

    test_season = Season("September 2024")
    test_result = [test_season.highest_tier(n) for n in test_counts]
    expected_result = [
        None,
        "Easy",
        "Easy",
        "Normal",
        "Normal",
        "Hard",
        "Hard",
        "Visionary",
    ]
    assert test_result == expected_result

    test_season = Season("August 2024")
    test_result = [test_season.highest_tier(n) for n in test_counts]
    expected_result = [
        None,
        None,
        "Easy",
        "Easy",
        "Normal",
        "Normal",
        "Hard",
        "Hard",
    ]
    assert test_result == expected_result


def text_next_tier():
    test_counts = [6, 8, 10, 12, 14, 16, 18, 22]

    test_season = Season("September 2024")
    test_result = [test_season.next_tier(n) for n in test_counts]

    expected_result = [
        {"name": "Easy", "increment": 2},
        {"name": "Normal", "increment": 4},
        {"name": "Normal", "increment": 2},
        {"name": "Hard", "increment": 4},
        {"name": "Hard", "increment": 2},
        {"name": "Visionary", "increment": 6},
        {"name": "Visionary", "increment": 4},
        None,
    ]
    assert test_result == expected_result

    test_season = Season("August 2024")
    test_result = [test_season.next_tier(n) for n in test_counts]
    expected_result = [
        {"name": "Easy", "increment": 4},
        {"name": "Easy", "increment": 2},
        {"name": "Normal", "increment": 4},
        {"name": "Normal", "increment": 2},
        {"name": "Hard", "increment": 4},
        {"name": "Hard", "increment": 2},
        None,
        None,
    ]
    assert test_result == expected_result
