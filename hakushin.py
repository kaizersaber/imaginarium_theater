import cloudscraper
import json
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from load_data import file_path, character_id_to_name
from timer import PerfProcTimer


HAKUSHIN_PATH = "https://api.hakush.in/gi"
HAKUSHIN_DATA_PATH = f"{HAKUSHIN_PATH}/data"

CHARACTER_JSON = "character.json"
SEASON_JSON = "rolecombat.json"

CHARACTER_FILE = "characters.csv"
SEASON_FILE = "seasons.csv"

scraper = cloudscraper.create_scraper()


def scrape_to_csvs():
    timer = PerfProcTimer("Retrieving data from Hakushin...")
    character_df = scrape_character_data()
    character_df.to_csv(file_path(CHARACTER_FILE), index=False)
    season_df = scrape_season_data()
    season_df.to_csv(file_path(SEASON_FILE), index=False)
    timer.end(f"Updated {CHARACTER_FILE} and {SEASON_FILE}")


def scrape_character_data() -> pd.DataFrame:
    response = scraper.get(f"{HAKUSHIN_DATA_PATH}/{CHARACTER_JSON}")
    str_response = str(response.content.decode("utf-8"))
    characters: dict = json.loads(str_response)
    excluded_chars = ["Traveler", "Manekin", "Manekina"]
    df = pd.DataFrame(
        columns=["character", "id", "star", "element", "img_path"],
        data=[
            (
                v["EN"],
                k,
                _star_rating(v["rank"]),
                v["element"],
                f"{v["icon"]}.webp",
            )
            for k, v in characters.items()
            if v["EN"] not in excluded_chars
        ],
    )
    df = df.sort_values("character")
    return df


def _star_rating(rank: str) -> int:
    rank_map = {
        "QUALITY_ORANGE": 5,
        "QUALITY_ORANGE_SP": 5,
        "QUALITY_PURPLE": 4,
    }
    return rank_map[rank]


def scrape_season_data() -> pd.DataFrame:
    response = scraper.get(f"{HAKUSHIN_DATA_PATH}/{SEASON_JSON}")
    str_response = str(response.content.decode("utf-8"))
    seasons: dict = json.loads(str_response)
    character_name = character_id_to_name()
    df = pd.DataFrame(
        columns=[
            "date",
            *(f"alt_cast_element_{i+1}" for i in range(3)),
            *(f"op_character_{i+1}" for i in range(6)),
            *(f"special_invite_{i+1}" for i in range(4)),
        ],
        data=[
            (
                _season_month(int(k)),
                *(_element_name(v["element"][i]) for i in range(3)),
                *(character_name[v["buff"][i]] for i in range(6)),
                *(character_name[v["invite"][i]] for i in range(4)),
            )
            for k, v in seasons.items()
        ],
    )
    df = df.sort_values("date", ascending=False)
    return df


def _element_name(id: int) -> str:
    id_to_name = {
        2: "Pyro",
        3: "Hydro",
        4: "Dendro",
        5: "Electro",
        6: "Cryo",
        7: "Anemo",
        8: "Geo",
    }
    return id_to_name[id]


def _season_month(x: int) -> date:
    FIRST_SEASON_DATE = date(2024, 7, 1)
    return FIRST_SEASON_DATE + relativedelta(months=x - 3)
