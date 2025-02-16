import requests
import re
import ast
import pandas as pd
from datetime import datetime, date
from load_data import file_path, character_id_to_name, element_label
from timer import PerfProcTimer

HOMDGCAT_WIKI_PATH = "https://homdgcat.wiki/gi/EN"

CHARACTER_FILE = "characters.csv"
SEASON_FILE = "seasons.csv"


def write_to_csvs():
    timer = PerfProcTimer("Retrieving data from HomDGCat Wiki...")
    character_df = scrape_character_data()
    character_df.to_csv(file_path(CHARACTER_FILE), index=False)
    season_df = scrape_season_data()
    season_df.to_csv(file_path(SEASON_FILE), index=False)
    timer.end(f"Updated {CHARACTER_FILE} and {SEASON_FILE}")


def scrape_character_data() -> pd.DataFrame:
    response = requests.get(f"{HOMDGCAT_WIKI_PATH}/avatar.js")
    str_response = str(response.content.decode("utf-8"))
    pattern = "_AvatarInfoConfig = (.*?)\n\nvar"
    str_list = re.findall(pattern, str_response, re.DOTALL)[0]
    character_list = ast.literal_eval(str_list)
    elem_label = element_label(invert=True)
    df = pd.DataFrame(
        columns=["character", "id", "element", "img_path"],
        data=[
            (c["Name"], c["_id"], elem_label[c["Element"]], f"{c["Icon"]}.png")
            for c in character_list
        ],
    )
    df = df[df["character"] != "Traveler"].sort_values("character")
    return df


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
    elem_label = element_label(invert=True)
    return [[elem_label[e] for e in s["Elem"]] for s in seasons]


def _scrape_characters_from(seasons: list) -> tuple[list[str], list[str]]:
    id_to_name = character_id_to_name()
    op_characters = [[id_to_name[c["ID"]] for c in s["Initial"]] for s in seasons]
    special_invites = [[id_to_name[c["ID"]] for c in s["Invitation"]] for s in seasons]
    return op_characters, special_invites


def _build_season_df(season_data: tuple[list, list, list, list]) -> pd.DataFrame:
    season_df = pd.DataFrame(
        [[date] + elem + op + spec for date, elem, op, spec in season_data],
        columns=["date"]
        + ["alt_cast_element_" + str(i + 1) for i in range(0, 3)]
        + ["op_character_" + str(i + 1) for i in range(0, 6)]
        + ["special_invite_" + str(i + 1) for i in range(0, 4)],
    )
    return season_df.sort_values("date", ascending=False)
