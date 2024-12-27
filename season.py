from datetime import datetime
import load_data
import pandas as pd


class Season:
    def __init__(self, date_label: str):
        self.date = datetime.strptime(date_label, "%B %Y").date()
        date_num = self.date.strftime("%Y%m")
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

    def get_element_img_paths(self):
        img_paths = load_data.element_img_paths()
        return [img_paths[e] for e in self.alt_cast_elements]

    def get_op_character_img_paths(self):
        img_paths = load_data.character_img_paths()
        return [img_paths[e] for e in self.op_characters]

    def get_special_invite_img_paths(self):
        img_paths = load_data.character_img_paths()
        return [img_paths[e] for e in self.special_invites]

    def count_elig_characters_in(self, character_inventory: list[str]):
        return len(self.get_elig_characters_in(character_inventory))

    def get_elig_characters_in(self, character_inventory: list[str]):
        modified_inventory = character_inventory + [
            c for c in self.op_characters if c not in character_inventory
        ]

        characters = load_data.characters()
        available_characters = characters[
            characters["character"].isin(modified_inventory)
        ]

        eligible_characters = available_characters[
            available_characters["element"].isin(self.alt_cast_elements)
            | available_characters["character"].isin(self.special_invites)
        ]["character"].tolist()

        if "Traveler" in character_inventory:
            eligible_characters += ["Traveler"]

        return eligible_characters

    def get_elig_character_imgs_in(self, inventory: list[str], traveler_name: str):
        img_paths = load_data.character_img_paths()
        selected_characters = self.get_elig_characters_in(inventory)
        selected_img_paths = [
            img_paths[e] for e in selected_characters if e != "Traveler"
        ]
        if "Traveler" in inventory:
            selected_img_paths += [load_data.traveler_img_path(traveler_name)]

        return selected_img_paths

    def highest_tier(self, n_chars: int):
        if self.date < datetime(2024, 9, 1).date():
            tier_counts = [10, 14, 18]
        else:
            tier_counts = [8, 12, 16, 22]

        tier_names = ["Easy", "Normal", "Hard", "Visionary"][0 : len(tier_counts)]
        tier_mask = [n_chars >= x for x in tier_counts]
        valid_tiers = [name for name, include in zip(tier_names, tier_mask) if include]
        if len(valid_tiers) > 0:
            return valid_tiers[-1]
        else:
            return "None"
