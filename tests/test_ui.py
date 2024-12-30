from ui_elements import _convert_GOOD_to_list


def test_convert_GOOD_to_list():
    test_json = {"characters": [{"key": "TravelerGeo", "level": 70}]}
    assert _convert_GOOD_to_list(test_json) == ["Traveler"]

    test_json = {"characters": [{"key": "TravelerElectro", "level": 69}]}
    assert _convert_GOOD_to_list(test_json) == []

    test_json = {
        "characters": [
            {"key": "TravelerDendro", "level": 70},
            {"key": "TravelerAnemo", "level": 70},
        ]
    }
    assert _convert_GOOD_to_list(test_json) == ["Traveler"]

    test_json = {
        "characters": [
            {"key": "TravelerHydro", "level": 70},
            {"key": "TravelerPyro", "level": 69},
        ]
    }
    assert _convert_GOOD_to_list(test_json) == ["Traveler"]

    test_json = {
        "characters": [
            {"key": "KamisatoAyaka", "level": 70},
            {"key": "KaedeharaKazuha", "level": 69},
            {"key": "KukiShinobu", "level": 70},
        ]
    }
    expected_result = ["Kamisato Ayaka", "Kuki Shinobu"]
    assert _convert_GOOD_to_list(test_json) == expected_result
