import pandas as pd

DATA_DIR = "data"


def characters():
    return pd.read_csv(f"{DATA_DIR}/characters.csv")


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
    return pd.read_csv(f"{DATA_DIR}/seasons.csv", dtype=str)
