import pandas as pd
from pathlib import Path
from datetime import datetime, date

GI_WIKI_IMG_PATH = "https://static.wikia.nocookie.net/gensin-impact/images"


def file_path(path: str) -> str:
    return Path(__file__).parent / path


def characters() -> pd.DataFrame:
    return pd.read_csv(file_path("characters.csv"))


def character_names() -> list[str]:
    return characters()["character"].tolist()


def character_keys() -> dict:
    return {n.replace(" ", ""): n for n in character_names()}


def element_img_paths() -> dict:
    return {
        "Anemo": f"{GI_WIKI_IMG_PATH}/1/10/Element_Anemo.svg",
        "Cryo": f"{GI_WIKI_IMG_PATH}/7/72/Element_Cryo.svg",
        "Dendro": f"{GI_WIKI_IMG_PATH}/7/73/Element_Dendro.svg",
        "Electro": f"{GI_WIKI_IMG_PATH}/f/ff/Element_Electro.svg",
        "Geo": f"{GI_WIKI_IMG_PATH}/9/9b/Element_Geo.svg",
        "Hydro": f"{GI_WIKI_IMG_PATH}/8/80/Element_Hydro.svg",
        "Pyro": f"{GI_WIKI_IMG_PATH}/2/2c/Element_Pyro.svg",
    }


def character_img_paths() -> dict:
    character_df = characters()
    names = character_df["character"].tolist()
    img_paths = (GI_WIKI_IMG_PATH + character_df["img_path"]).tolist()
    return {n: p for n, p in zip(names, img_paths)}


def traveler_img_path(player_choice: str) -> str:
    if player_choice == "Aether":
        return f"{GI_WIKI_IMG_PATH}/a/a5/Aether_Icon.png"
    elif player_choice == "Lumine":
        return f"{GI_WIKI_IMG_PATH}/9/9c/Lumine_Icon.png"


def season_labels() -> list[str]:
    season_dates = seasons()["date"].tolist()
    return [datetime.strftime(d, "%B %Y") for d in season_dates]


def seasons() -> list[date]:
    seasons = pd.read_csv(file_path("seasons.csv"), dtype=str)
    seasons["date"] = [datetime.strptime(d, "%Y-%m-%d").date() for d in seasons["date"]]
    return seasons
