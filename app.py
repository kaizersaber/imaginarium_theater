from shiny import ui, reactive, App, render
from datetime import datetime
import json

import load_data
from season import Season
from ui_elements import ui_imgs, ui_update_inventory

app_ui = ui.page_fluid(
    ui.head_content(ui.tags.title("Imaginarium Theater")),
    ui.input_dark_mode(),
    ui.tags.link(
        rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Newsreader"
    ),
    ui.tags.style("body { font-family: 'Newsreader'}"),
    ui.tags.style(".tooltip { background-color: black; font-family: 'Newsreader'}"),
    ui.row(
        ui.panel_title("Imaginarium Theater"),
        ui.div(
            ui.input_selectize(
                id="selected_season",
                label="",
                choices=load_data.season_labels(),
                selected=datetime.today().strftime("%B %Y"),
                width="170px",
            )
        ),
        align="center",
    ),
    ui.row(
        ui.column(
            4,
            ui.panel_title("Alternate Cast Elements"),
            ui.output_ui(id="selected_season_alt_cast_elements"),
            align="center",
        ),
        ui.column(
            4,
            ui.panel_title("Opening Characters"),
            ui.output_ui(id="selected_season_op_characters"),
            align="center",
        ),
        ui.column(
            4,
            ui.panel_title("Special Invitations"),
            ui.output_ui(id="selected_season_special_invites"),
            align="center",
        ),
    ),
    ui.p(),
    ui.row(
        ui.panel_title("Character Inventory"),
        ui.help_text(
            "Genshin Open Object Definition (GOOD) format is accepted, "
            + " note that characters under level 70 are automatically excluded"
        ),
        ui.div(
            ui.input_file(
                id="import_inventory",
                label="",
                button_label="Import characters from .json",
                accept=".json",
                width="500px",
            )
        ),
        ui.row(
            ui.column(
                6,
                ui.input_checkbox(
                    id="include_traveler",
                    label="Include Traveler?",
                    value=True,
                ),
                align="right",
                style="margin-top:6px",
            ),
            ui.column(
                6,
                ui.input_selectize(
                    id="traveler_name",
                    label="",
                    choices=["Aether", "Lumine"],
                    width="150px",
                ),
                align="left",
            ),
        ),
        ui.input_selectize(
            id="character_inventory",
            label="Type in box to search for character names",
            choices=load_data.character_names(),
            multiple=True,
            width="100%",
        ),
        ui.help_text("Exports to a simple array format usable for this page"),
        ui.div(
            ui.download_button(
                id="export_inventory", label="Export characters to .json"
            )
        ),
        ui.p(),
        ui.panel_title("Character Requirement Counter"),
        ui.output_text(id="difficulty_text"),
        ui.output_text(id="eligible_characters_text"),
        ui.row(
            ui.column(
                2,
                ui.output_text(id="breakdown_elem_text_1"),
                ui.div(ui.output_ui(id="breakdown_elem_imgs_1")),
                style="padding:0px",
            ),
            ui.column(
                2,
                ui.output_text(id="breakdown_elem_text_2"),
                ui.div(ui.output_ui(id="breakdown_elem_imgs_2")),
                style="padding:0px",
            ),
            ui.column(
                2,
                ui.output_text(id="breakdown_elem_text_3"),
                ui.div(ui.output_ui(id="breakdown_elem_imgs_3")),
                style="padding:0px",
            ),
            ui.column(
                2,
                ui.output_text(id="breakdown_op_text"),
                ui.div(ui.output_ui(id="breakdown_op_imgs")),
                style="padding:0px",
            ),
            ui.column(
                2,
                ui.output_text(id="breakdown_special_invite_text"),
                ui.div(ui.output_ui(id="breakdown_special_invite_imgs")),
                style="padding:0px",
            ),
            ui.column(
                2,
                ui.output_text(id="breakdown_traveler_text"),
                ui.div(ui.output_ui(id="breakdown_traveler_img")),
                style="padding:0px",
            ),
        ),
        ui.p(),
        ui.p(
            "Made by ",
            ui.tags.a(
                "xSaberFaye",
                href="https://www.youtube.com/@xsaberfaye",
                target="_blank",
            ),
            " - Season information from ",
            ui.tags.a(
                "HomDGCat Wiki",
                href="https://homdgcat.wiki/gi/maze?lang=EN",
                target="_blank",
            ),
            " - Image assets from ",
            ui.tags.a(
                "Genshin Impact Wiki",
                href="https://genshin-impact.fandom.com/wiki/Character/List",
                target="_blank",
            ),
            " - View source code on ",
            ui.tags.a(
                "Github",
                href="https://github.com/kaizersaber/imaginarium_theater",
                target="_blank",
            ),
        ),
        align="center",
    ),
)


def server(input, output, session):
    @render.ui
    def selected_season_alt_cast_elements() -> ui.TagList:
        selected_img_paths = selected_season().get_element_imgs()
        return ui_imgs(selected_img_paths, width="50px")

    @render.ui
    def selected_season_op_characters() -> ui.TagList:
        selected_img_paths = selected_season().get_op_character_imgs()
        return ui_imgs(selected_img_paths, width="50px")

    @render.ui
    def selected_season_special_invites() -> ui.TagList:
        selected_img_paths = selected_season().get_special_invite_imgs()
        return ui_imgs(selected_img_paths, width="50px")

    @reactive.calc
    def selected_season() -> Season:
        return Season(input.selected_season())

    @render.download(
        filename=(
            "character_inventory_"
            + datetime.today().date().strftime("%Y-%m-%d")
            + ".json"
        )
    )
    def export_inventory():
        yield json.dumps(character_inventory()).encode("utf-8")

    @reactive.calc
    def character_inventory() -> list[str]:
        inventory = list(input.character_inventory())
        if input.include_traveler():
            inventory += ["Traveler"]
        return inventory

    @reactive.effect
    def import_inventory():
        file = input.import_inventory()
        if file is not None:
            with open(file[0]["datapath"], "r") as f:
                inventory = json.load(f)
            ui_update_inventory(ui, inventory)

    @render.text
    def difficulty_text() -> str:
        season = selected_season()
        count = season.count_elig_characters_in(character_inventory())
        current_tier_name = season.highest_tier(count)
        next_tier = season.next_tier(count)
        if current_tier_name is None:
            text = f"You do not have enough characters to participate this season."
        else:
            text = f"The highest difficulty you can challenge this season is {current_tier_name}."

        if next_tier is None:
            text += " You have reached the highest difficulty tier this season."
        else:
            increment = next_tier["increment"]
            suffix = "s" if increment > 1 else ""
            text += f" You need {next_tier["increment"]} more character{suffix} "
            text += f"to challenge {next_tier["name"]} difficulty."

        return text

    @reactive.calc
    def elig_char_breakdown() -> dict:
        return selected_season().get_elig_char_breakdown_in(
            character_inventory(), input.traveler_name()
        )

    @render.text
    def eligible_characters_text() -> str:
        count = count_elig_characters_in(elig_char_breakdown())
        return f"You have {count} eligible characters this season:"

    def count_elig_characters_in(breakdown: dict) -> int:
        breakdown = elig_char_breakdown()
        return sum([len(breakdown[section]["characters"]) for section in breakdown])

    @render.ui
    def breakdown_elem_imgs_1() -> ui.TagList:
        return imgs_if_section_in_breakdown("element_1", elig_char_breakdown())

    @render.text
    def breakdown_elem_text_1() -> str:
        count = count_if_section_in_breakdown("element_1", elig_char_breakdown())
        return f"{count} from {selected_season().alt_cast_elements[0]}"

    @render.ui
    def breakdown_elem_imgs_2() -> ui.TagList:
        return imgs_if_section_in_breakdown("element_2", elig_char_breakdown())

    @render.text
    def breakdown_elem_text_2() -> str:
        count = count_if_section_in_breakdown("element_2", elig_char_breakdown())
        return f"{count} from {selected_season().alt_cast_elements[1]}"

    @render.ui
    def breakdown_elem_imgs_3() -> ui.TagList:
        return imgs_if_section_in_breakdown("element_3", elig_char_breakdown())

    @render.text
    def breakdown_elem_text_3() -> str:
        count = count_if_section_in_breakdown("element_3", elig_char_breakdown())
        return f"{count} from {selected_season().alt_cast_elements[2]}"

    @render.ui
    def breakdown_op_imgs() -> ui.TagList:
        return imgs_if_section_in_breakdown("op", elig_char_breakdown())

    @render.text
    def breakdown_op_text() -> str:
        count = count_if_section_in_breakdown("op", elig_char_breakdown())
        return f"{count} from Opening Characters"

    @render.ui
    def breakdown_special_invite_imgs() -> ui.TagList:
        return imgs_if_section_in_breakdown("special_invites", elig_char_breakdown())

    @render.text
    def breakdown_special_invite_text() -> str:
        count = count_if_section_in_breakdown("special_invites", elig_char_breakdown())
        return f"{count} from Special Invitations"

    @render.ui
    def breakdown_traveler_img() -> ui.TagList:
        return imgs_if_section_in_breakdown("traveler", elig_char_breakdown())

    @render.text
    def breakdown_traveler_text() -> str:
        count = count_if_section_in_breakdown("traveler", elig_char_breakdown())
        cluding = "including" if input.include_traveler() else "excluding"
        return f"{count} from {cluding} {input.traveler_name()}"

    def imgs_if_section_in_breakdown(
        section: str, breakdown: dict, width: str = "50px"
    ) -> ui.TagList:
        if section in breakdown:
            selected_imgs = breakdown[section]["img_names_and_paths"]
            return ui_imgs(selected_imgs, width="50px")
        else:
            return ui.TagList()

    def count_if_section_in_breakdown(section: str, breakdown: dict) -> int:
        return len(breakdown[section]["characters"]) if section in breakdown else 0


app = App(app_ui, server)
