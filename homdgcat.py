import requests
import re
import ast
import pandas as pd
from datetime import datetime

HOMDGCAT_WIKI_PATH = "https://homdgcat.wiki/gi/EN"


def seasons_to_csv():
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

    season_df = season_df.sort_values("date", ascending=False).reset_index(drop=True)
    season_df.to_csv("seasons.csv", index=False)
    return season_df


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
