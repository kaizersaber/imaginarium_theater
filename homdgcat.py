import requests
import re
import ast
import pandas as pd
from datetime import datetime, date
from load_data import file_path
from timer import PerfProcTimer

HOMDGCAT_WIKI_PATH = "https://homdgcat.wiki/gi/EN"


def write_seasons_to_csv(file_name: str) -> pd.DataFrame:
    timer = PerfProcTimer("Pulling season information from HomDGCat Wiki...")
    season_df = scrape_season_data()
    season_df.to_csv(file_path(file_name), index=False)
    timer.end(f"Season information written to {file_name}")
    return season_df


def scrape_season_data() -> pd.DataFrame:
    season_dates, season_elem_chars = _get_season_info()
    dates = _scrape_dates_from(season_dates)
    alt_cast_elements = _scrape_elements_from(season_elem_chars)
    op_characters, special_invites = _scrape_characters_from(season_elem_chars)
    season_df = _build_season_df(
        zip(dates, alt_cast_elements, op_characters, special_invites)
    )
    return season_df


def _get_season_info() -> tuple[list, list]:
    response = requests.get(f"{HOMDGCAT_WIKI_PATH}/maze.js")
    str_response = str(response.content.decode("utf-8"))
    season_dates = _find_in(str_response, pattern="_plane = (.*?)\n\nvar")
    season_elem_chars = _find_in(str_response, pattern="_overall = (.*?)\n\nvar")
    return season_dates, season_elem_chars


def _find_in(response: str, pattern: str) -> list:
    str_list = re.findall(pattern, response, re.DOTALL)[0]
    return ast.literal_eval(str_list)


def _scrape_dates_from(seasons: list) -> list[date]:
    dates = [datetime.strptime(s["Time"], "%Y/%m").date() for s in seasons]
    return dates


def _scrape_elements_from(seasons: list) -> list[str]:
    element_labels = _element_labels()
    return [[element_labels[e] for e in s["Elem"]] for s in seasons]


def _element_labels() -> dict[str, str]:
    element_labels = {
        "Fire": "Pyro",
        "Water": "Hydro",
        "Ice": "Cryo",
        "Elec": "Electro",
        "Grass": "Dendro",
        "Wind": "Anemo",
        "Rock": "Geo",
    }
    return element_labels


def _scrape_characters_from(seasons: list) -> tuple[list[str], list[str]]:
    character_ids = _character_ids()
    op_characters = [[character_ids[c["ID"]] for c in s["Initial"]] for s in seasons]
    special_invites = [
        [character_ids[c["ID"]] for c in s["Invitation"]] for s in seasons
    ]
    return op_characters, special_invites


def _character_ids() -> dict[int, str]:
    response = requests.get(f"{HOMDGCAT_WIKI_PATH}/avatar.js")
    str_response = str(response.content.decode("utf-8"))
    pattern = "_AvatarInfoConfig = (.*?)\n\nvar"
    str_list = re.findall(pattern, str_response, re.DOTALL)[0]
    character_list = ast.literal_eval(str_list)
    return {c["_id"]: c["Name"] for c in character_list}


def _build_season_df(season_data: tuple[list, list, list, list]) -> pd.DataFrame:
    season_df = pd.DataFrame(
        [[date] + elem + op + spec for date, elem, op, spec in season_data],
        columns=["date"]
        + ["alt_cast_element_" + str(i + 1) for i in range(0, 3)]
        + ["op_character_" + str(i + 1) for i in range(0, 6)]
        + ["special_invite_" + str(i + 1) for i in range(0, 4)],
    )
    return season_df.sort_values("date", ascending=False)
