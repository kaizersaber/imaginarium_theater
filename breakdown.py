from shiny import ui
from ui_elements import ui_imgs


class Breakdown:
    sections = [f"element_{i}" for i in [1, 2, 3]] + [
        "op",
        "special_invites",
        "traveler",
    ]

    def __init__(self, d: dict):
        self.d = d

    def n_chars(self, section: str | None = None) -> int:
        return sum([self.n_chars_in_section(s) for s in self.d])

    def n_chars_in_section(self, section: str) -> int:
        return len(self.d[section]["characters"]) if section in self.d else 0

    def ui_imgs_in_section(self, section: str, width: str = "50px") -> ui.TagList:
        if section in self.d:
            selected_imgs = self.d[section]["img_names_and_paths"]
            return ui_imgs(selected_imgs, width=width)
        else:
            return ui.TagList()
