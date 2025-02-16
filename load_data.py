import pandas as pd
from pathlib import Path
from datetime import datetime, date

HOMDGCAT_RES_PATH = "https://homdgcat.wiki/homdgcat-res"
HOMDGCAT_ELEM_IMG_PATH = f"{HOMDGCAT_RES_PATH}/Csxylic"
HOMDGCAT_CHAR_IMG_PATH = f"{HOMDGCAT_RES_PATH}/Avatar"


def file_path(path: str) -> str:
    return Path(__file__).parent / path


def characters() -> pd.DataFrame:
    return pd.read_csv(file_path("characters.csv"))


def character_names() -> list[str]:
    return characters()["character"].tolist()


def character_keys() -> dict:
    return {n.replace(" ", ""): n for n in character_names()}


def element_img_paths() -> dict:
    elements = pd.unique(characters()["element"])
    elem_label = element_label()
    img_paths = {e: f"{HOMDGCAT_ELEM_IMG_PATH}/{elem_label[e]}.png" for e in elements}
    return img_paths


def element_label(invert: bool = False) -> dict[str]:
    elements = {
        "Electro": "Elec",
        "Anemo": "Wind",
        "Cryo": "Ice",
        "Pyro": "Fire",
        "Geo": "Rock",
        "Hydro": "Water",
        "Dendro": "Grass",
    }
    if invert:
        elements = {v: k for k, v in elements.items}
    return elements


def character_id_to_name() -> dict:
    character_df = characters()
    ids = character_df["id"].tolist()
    names = character_df["character"].tolist()
    return {i: n for i, n in zip(ids, names)}


def character_img_paths() -> dict:
    character_df = characters()
    names = character_df["character"].tolist()
    img_paths = [
        f"{HOMDGCAT_CHAR_IMG_PATH}/{path}" for path in character_df["img_path"]
    ]
    return {n: p for n, p in zip(names, img_paths)}


def traveler_img_path(player_choice: str) -> str:
    if player_choice == "Aether":
        return f"{HOMDGCAT_CHAR_IMG_PATH}/UI_AvatarIcon_PlayerBoy.png"
    elif player_choice == "Lumine":
        return f"{HOMDGCAT_CHAR_IMG_PATH}/UI_AvatarIcon_PlayerGirl.png"


def season_labels() -> list[str]:
    season_dates = seasons()["date"].tolist()
    return [datetime.strftime(d, "%B %Y") for d in season_dates]


def seasons() -> list[date]:
    seasons = pd.read_csv(file_path("seasons.csv"), dtype=str)
    seasons["date"] = [datetime.strptime(d, "%Y-%m-%d").date() for d in seasons["date"]]
    return seasons
