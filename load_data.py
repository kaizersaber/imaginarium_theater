import pandas as pd
from pathlib import Path
from datetime import datetime


def file_path(path: str):
    return Path(__file__).parent / path


def characters():
    return pd.read_csv(file_path("characters.csv"))


def character_names():
    return characters()["character"].tolist()


def elements():
    return [
        "Anemo",
        "Cryo",
        "Dendro",
        "Electro",
        "Geo",
        "Hydro",
        "Pyro",
    ]


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
