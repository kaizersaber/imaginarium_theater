import pandas as pd
import requests
import re
import ast
from pathlib import Path
from datetime import datetime

GI_WIKI_PATH = "https://static.wikia.nocookie.net/gensin-impact/images"
HOMDGCAT_WIKI_PATH = "https://homdgcat.wiki/gi/EN"


def file_path(path: str):
    return Path(__file__).parent / path


def characters():
    return pd.read_csv(file_path("characters.csv"))


def character_names():
    return characters()["character"].tolist()


def character_keys():
    return {n.replace(" ", ""): n for n in character_names()}


def element_img_paths():
    return {
        "Anemo": f"{GI_WIKI_PATH}/1/10/Element_Anemo.svg",
        "Cryo": f"{GI_WIKI_PATH}/7/72/Element_Cryo.svg",
        "Dendro": f"{GI_WIKI_PATH}/7/73/Element_Dendro.svg",
        "Electro": f"{GI_WIKI_PATH}/f/ff/Element_Electro.svg",
        "Geo": f"{GI_WIKI_PATH}/9/9b/Element_Geo.svg",
        "Hydro": f"{GI_WIKI_PATH}/8/80/Element_Hydro.svg",
        "Pyro": f"{GI_WIKI_PATH}/2/2c/Element_Pyro.svg",
    }


def character_img_paths():
    character_df = characters()
    names = character_df["character"].tolist()
    img_paths = (GI_WIKI_PATH + character_df["img_path"]).tolist()
    return {n: p for n, p in zip(names, img_paths)}


def traveler_img_path(player_choice: str):
    if player_choice == "Aether":
        return f"{GI_WIKI_PATH}/a/a5/Aether_Icon.png"
    elif player_choice == "Lumine":
        return f"{GI_WIKI_PATH}/9/9c/Lumine_Icon.png"


def seasons():
    season_list = _homdgcat_seasons()
    dates = [
        datetime.strptime(s["Time"].split(" -")[0], "%Y-%m-%d").date()
        for s in season_list
    ]
    element_labels = _homdgcat_element_labels()
    alt_cast_elements = [[element_labels[e] for e in s["Elem"]] for s in season_list]
    character_ids = _homdgcat_character_ids()
    op_characters = [
        [character_ids[c["ID"]] for c in s["Initial"]] for s in season_list
    ]
    special_invites = [
        [character_ids[c["ID"]] for c in s["Invitation"]] for s in season_list
    ]
    season_df = pd.DataFrame(
        columns=["date"]
        + ["alt_cast_element_" + str(i + 1) for i in range(0, 3)]
        + ["op_character_" + str(i + 1) for i in range(0, 6)]
        + ["special_invite_" + str(i + 1) for i in range(0, 4)]
    )
    for i in range(0, len(dates)):
        row_dict = {"date": dates[i]}
        row_dict.update(
            {
                "alt_cast_element_" + str(j + 1): alt_cast_elements[i][j]
                for j in range(0, 3)
            }
        )
        row_dict.update(
            {"op_character_" + str(j + 1): op_characters[i][j] for j in range(0, 6)}
        )
        row_dict.update(
            {"special_invite_" + str(j + 1): special_invites[i][j] for j in range(0, 4)}
        )
        season_row = pd.DataFrame(row_dict, index=[i])
        season_df = pd.concat([season_df, season_row], ignore_index=True)
    return season_df.sort_values("date", ascending=False).reset_index(drop=True)


def _homdgcat_seasons():
    response = requests.get(f"{HOMDGCAT_WIKI_PATH}/maze.js")
    str_response = str(response.content.decode("utf-8"))
    pattern = "_overall = (.*?)\n\nvar"
    str_list = re.findall(pattern, str_response, re.DOTALL)[0]
    season_list = ast.literal_eval(str_list)
    return season_list


def _homdgcat_element_labels():
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


def _homdgcat_character_ids():
    response = requests.get(f"{HOMDGCAT_WIKI_PATH}/avatar.js")
    str_response = str(response.content.decode("utf-8"))
    pattern = "_AvatarInfoConfig = (.*?)\n\nvar"
    str_list = re.findall(pattern, str_response, re.DOTALL)[0]
    character_list = ast.literal_eval(str_list)
    return {c["_id"]: c["Name"] for c in character_list}


def season_labels():
    return [datetime.strftime(d, "%B %Y") for d in season_dates()]


def season_dates():
    return seasons()["date"].tolist()
