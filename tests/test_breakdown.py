from breakdown import Breakdown


def test_n_chars():
    assert _make_test_breakdown().n_chars() == 6


def test_n_chars_in_section():
    test_result = [
        _make_test_breakdown().n_chars_in_section(s) for s in Breakdown.sections
    ]
    expected_result = [1, 0, 2, 3, 0, 0]
    assert test_result == expected_result


def _make_test_breakdown() -> Breakdown:
    return Breakdown(
        {
            "element_1": {"characters": ["Kaeya"]},
            "element_3": {"characters": ["Yanfei", "Gaming"]},
            "op": {"characters": ["Keqing", "Furina", "Ororon"]},
        }
    )
