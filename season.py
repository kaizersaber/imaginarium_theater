from datetime import datetime
import load_data
import pandas as pd


class Season:
    def __init__(self, date_label: str):
        self.date = datetime.strptime(date_label, "%B %Y").date()
        date_num = datetime.strftime(self.date, "%Y%m")
        seasons = load_data.seasons()
        selected_season = seasons[seasons["date"] == date_num].melt(
            id_vars=["date"], var_name="field"
        )
        self.alt_cast_elements = Season._pull_alt_cast_elements_from(selected_season)
        self.special_invites = Season._pull_special_invites_from(selected_season)
        self.op_characters = Season._pull_op_characters_from(selected_season)

    def _pull_alt_cast_elements_from(df: pd.DataFrame):
        return Season._df_field_to_list(df, "alt_cast_element")

    def _pull_special_invites_from(df: pd.DataFrame):
        return Season._df_field_to_list(df, "special_invite")

    def _pull_op_characters_from(df: pd.DataFrame):
        return Season._df_field_to_list(df, "op_character")

    def _df_field_to_list(df: pd.DataFrame, field_name: str):
        return df[df["field"].str.contains(field_name)]["value"].tolist()

    def count_elig_characters_in(self, character_inventory: list[str]):
        return len(self.get_elig_characters_in(character_inventory))

    def get_elig_characters_in(self, character_inventory: list[str]):
        character_inventory += [
            c for c in self.op_characters if c not in character_inventory
        ]

        characters = load_data.characters()
        available_characters = characters[
            characters["character"].isin(character_inventory)
        ]

        eligible_characters = available_characters[
            available_characters["element"].isin(self.alt_cast_elements)
            | available_characters["character"].isin(self.special_invites)
        ]["character"].tolist()

        if "Traveler" in character_inventory:
            eligible_characters += ["Traveler"]

        return eligible_characters
