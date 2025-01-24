from datetime import datetime
import load_data
import pandas as pd


class Season:
    def __init__(self, date_label: str):
        self.date = datetime.strptime(date_label, "%B %Y").date()
        seasons = load_data.seasons()
        selected_season = seasons[seasons["date"] == self.date].melt(
            id_vars=["date"], var_name="field"
        )
        self.alt_cast_elements = Season._pull_alt_cast_elements_from(selected_season)
        self.special_invites = Season._pull_special_invites_from(selected_season)
        self.op_characters = Season._pull_op_characters_from(selected_season)

    def _pull_alt_cast_elements_from(df: pd.DataFrame) -> list[str]:
        return Season._df_field_to_list(df, "alt_cast_element")

    def _pull_special_invites_from(df: pd.DataFrame) -> list[str]:
        return Season._df_field_to_list(df, "special_invite")

    def _pull_op_characters_from(df: pd.DataFrame) -> list[str]:
        return Season._df_field_to_list(df, "op_character")

    def _df_field_to_list(df: pd.DataFrame, field_name: str) -> list[str]:
        return df[df["field"].str.contains(field_name)]["value"].tolist()

    def get_element_imgs(self) -> tuple[str, str]:
        img_paths = load_data.element_img_paths()
        selected_paths = [img_paths[e] for e in self.alt_cast_elements]
        return zip(self.alt_cast_elements, selected_paths)

    def get_op_character_imgs(self) -> tuple[str, str]:
        img_paths = load_data.character_img_paths()
        selected_paths = [img_paths[c] for c in self.op_characters]
        return zip(self.op_characters, selected_paths)

    def get_special_invite_imgs(self) -> tuple[str, str]:
        img_paths = load_data.character_img_paths()
        selected_paths = [img_paths[c] for c in self.special_invites]
        return zip(self.special_invites, selected_paths)

    def count_elig_characters_in(self, inventory: list[str]) -> int:
        breakdown = self.get_elig_char_breakdown_in(inventory)
        return sum([len(breakdown[section]["characters"]) for section in breakdown])

    def get_elig_char_breakdown_in(
        self, inventory: list[str], traveler_name: str = "Aether"
    ) -> list[list[str]]:
        breakdown = {}
        self._add_element_sections_to_breakdown(breakdown, inventory)
        self._add_op_and_special_invite_sections_to_breakdown(breakdown, inventory)
        if "Traveler" in inventory:
            self._add_traveler_section_to_breakdown(breakdown, traveler_name)

        return breakdown

    def _add_element_sections_to_breakdown(self, breakdown: dict, inventory: list[str]):
        characters = load_data.characters()
        chars_from_elements = [
            characters[
                characters["character"].isin(inventory) & (characters["element"] == e)
            ]["character"].tolist()
            for e in self.alt_cast_elements
        ]
        element_section = {
            f"element_{i+1}": {
                "characters": chars,
                "img_names_and_paths": Season._char_imgs(chars),
            }
            for i, chars in enumerate(chars_from_elements)
            if len(chars) > 0
        }
        breakdown.update(element_section)

    def _add_op_and_special_invite_sections_to_breakdown(
        self, breakdown: dict, inventory: list[str]
    ):
        chars_from_op = [c for c in self.op_characters if c not in inventory]
        chars_from_special_invite = [c for c in self.special_invites if c in inventory]
        sections_and_characters = zip(
            ["op", "special_invites"],
            [chars_from_op, chars_from_special_invite],
        )
        breakdown.update(
            {
                section: {
                    "characters": chars,
                    "img_names_and_paths": Season._char_imgs(chars),
                }
                for section, chars in sections_and_characters
                if len(chars) > 0
            }
        )

    def _add_traveler_section_to_breakdown(
        self, breakdown: dict, traveler_name: str = "Aether"
    ):
        traveler_section = {
            "traveler": {
                "characters": ["Traveler"],
                "img_names_and_paths": Season._char_imgs(["Traveler"], traveler_name),
            }
        }
        breakdown.update(traveler_section)

    def _char_imgs(characters: list[str], traveler_name: str = "Aether"):
        img_paths = load_data.character_img_paths()
        selected_img_names = [c for c in characters if c != "Traveler"]
        selected_img_paths = [img_paths[n] for n in selected_img_names]

        if "Traveler" in characters:
            selected_img_names += [traveler_name]
            selected_img_paths += [load_data.traveler_img_path(traveler_name)]

        return zip(selected_img_names, selected_img_paths)

    def highest_tier(self, n_chars: int) -> str | None:
        tier_names, tier_counts = self.get_tier_names_and_counts()
        valid_tiers = [name for name, i in zip(tier_names, tier_counts) if n_chars >= i]
        if len(valid_tiers) > 0:
            return valid_tiers[-1]
        else:
            return None

    def next_tier(self, n_chars: int) -> dict | None:
        tier_names, tier_counts = self.get_tier_names_and_counts()
        next_names = [name for name, i in zip(tier_names, tier_counts) if n_chars < i]
        next_increments = [i - n_chars for i in tier_counts if n_chars < i]
        if len(next_names) > 0:
            return {"name": next_names[0], "increment": next_increments[0]}
        else:
            return None

    def get_tier_names_and_counts(self) -> tuple[list[int], list[str]]:
        tier_counts = self.get_tier_counts()
        tier_names = self.get_tier_names(tier_counts)
        return tier_names, tier_counts

    def get_tier_counts(self) -> list[int]:
        if self.date < datetime(2024, 9, 1).date():
            return [10, 14, 18]
        else:
            return [8, 12, 16, 22]

    def get_tier_names(self, tier_counts: list[int]) -> list[str]:
        return ["Easy", "Normal", "Hard", "Visionary"][0 : len(tier_counts)]
