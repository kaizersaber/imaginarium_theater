import pandas as pd
from pathlib import Path
from datetime import datetime

SITE_PATH = "https://static.wikia.nocookie.net/gensin-impact/images"


def file_path(path: str):
    return Path(__file__).parent / path


def characters():
    return pd.read_csv(file_path("characters.csv"))


def character_names():
    return characters()["character"].tolist()


def element_img_paths():
    return {
        "Anemo": f"{SITE_PATH}/1/10/Element_Anemo.svg",
        "Cryo": f"{SITE_PATH}/7/72/Element_Cryo.svg",
        "Dendro": f"{SITE_PATH}/7/73/Element_Dendro.svg",
        "Electro": f"{SITE_PATH}/f/ff/Element_Electro.svg",
        "Geo": f"{SITE_PATH}/9/9b/Element_Geo.svg",
        "Hydro": f"{SITE_PATH}/8/80/Element_Hydro.svg",
        "Pyro": f"{SITE_PATH}/2/2c/Element_Pyro.svg",
    }


def character_img_paths():
    character_df = characters()
    names = character_df["character"].tolist()
    img_paths = (SITE_PATH + character_df["img_path"]).tolist()
    return {n: p for n, p in zip(names, img_paths)}


def traveler_img_path(player_choice: str):
    if player_choice == "Aether":
        return f"{SITE_PATH}/a/a5/Aether_Icon.png"
    elif player_choice == "Lumine":
        return f"{SITE_PATH}/9/9c/Lumine_Icon.png"


def seasons():
    return pd.read_csv(file_path("seasons.csv"), dtype=str)


def season_labels_and_dates():
    dates = seasons()["date"].tolist()
    dates = [datetime.strptime(d, "%Y%m").date() for d in dates]
    labels = [datetime.strftime(d, "%B %Y") for d in season_dates()]
    return dict(zip(labels, dates))


def season_dates():
    dates = seasons()["date"].tolist()
    return [datetime.strptime(d, "%Y%m").date() for d in dates]


def season_labels():
    return [datetime.strftime(d, "%B %Y") for d in season_dates()]
