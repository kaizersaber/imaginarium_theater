from shiny import ui, reactive, App, render
from datetime import datetime
from faicons import icon_svg
import json

import load_data
from season import Season
from breakdown import Breakdown
from ui_elements import (
    ui_season_info,
    ui_breakdown,
    ui_credits,
    ui_imgs,
    ui_update_inventory,
)

app_ui = ui.page_fluid(
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
    ui_season_info(),
    ui.p(),
    ui.row(
        ui.panel_title("Character Inventory"),
        ui.row(
            ui.column(
                4,
                ui.div(
                    ui.tooltip(
                        ui.input_file(
                            id="import_inventory",
                            label="Import Inventory",
                            button_label=icon_svg("upload"),
                            accept=".json",
                            placeholder="Click to upload .json file",
                        ),
                        "Genshin Open Object Definition (GOOD) format is accepted, "
                        + "characters under level 70 are automatically excluded",
                        placement="bottom",
                    )
                ),
                align="center",
            ),
            ui.column(
                4,
                "Customize Traveler",
                ui.p(),
                ui.row(
                    ui.column(
                        6,
                        ui.input_checkbox(
                            id="include_traveler",
                            label="Include ",
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
                            width="100px",
                        ),
                        align="left",
                    ),
                ),
            ),
            ui.column(
                4,
                "Export Inventory",
                ui.p(),
                ui.div(
                    ui.tooltip(
                        ui.download_button(
                            id="export_inventory", label=icon_svg("download")
                        ),
                        "Exports to a simple array .json usable for this page",
                        placement="bottom",
                    )
                ),
                align="center",
            ),
        ),
        ui.input_selectize(
            id="character_inventory",
            label="Type in box to search for character names",
            choices=load_data.character_names(),
            multiple=True,
            width="100%",
        ),
        ui.p(),
        ui.panel_title("Character Requirement Counter"),
        ui.output_text(id="highest_difficulty_text"),
        ui.output_text(id="next_difficulty_text"),
        ui.p(),
        ui.output_text(id="eligible_characters_text"),
        ui.p(),
        ui_breakdown(),
        ui.p(),
        ui_credits(),
        align="center",
    ),
    title="Imaginarium Theater",
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
        filename=(f"inventory_{datetime.today().strftime("%Y-%m-%d")}.json")
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
    def highest_difficulty_text() -> str:
        count = elig_char_breakdown().n_chars()
        highest_tier = selected_season().highest_tier(count)
        if highest_tier is None:
            text = f"You do not have enough characters to participate this season."
        else:
            text = f"The highest difficulty you can challenge this season is {highest_tier}."
        return text

    @render.text
    def next_difficulty_text() -> str:
        count = elig_char_breakdown().n_chars()
        next_tier = selected_season().next_tier(count)
        if next_tier is None:
            text = " You have reached the highest difficulty tier this season."
        else:
            increment = next_tier["increment"]
            suffix = "s" if increment > 1 else ""
            text = f" You need {next_tier["increment"]} more character{suffix} "
            text += f"to challenge {next_tier["name"]} difficulty."
        return text

    @reactive.calc
    def elig_char_breakdown() -> Breakdown:
        return selected_season().get_elig_char_breakdown_in(
            character_inventory(), input.traveler_name()
        )

    @render.text
    def eligible_characters_text() -> str:
        count = elig_char_breakdown().n_chars()
        return f"You have {count} eligible characters this season:"

    @render.text
    def breakdown_element_1_text() -> str:
        count = elig_char_breakdown().n_chars_in_section("element_1")
        return f"{count} from {selected_season().alt_cast_elements[0]}"

    @render.ui
    def breakdown_element_1_imgs() -> ui.TagList:
        return elig_char_breakdown().ui_imgs_in_section("element_1")

    @render.text
    def breakdown_element_2_text() -> str:
        count = elig_char_breakdown().n_chars_in_section("element_2")
        return f"{count} from {selected_season().alt_cast_elements[1]}"

    @render.ui
    def breakdown_element_2_imgs() -> ui.TagList:
        return elig_char_breakdown().ui_imgs_in_section("element_2")

    @render.text
    def breakdown_element_3_text() -> str:
        count = elig_char_breakdown().n_chars_in_section("element_3")
        return f"{count} from {selected_season().alt_cast_elements[2]}"

    @render.ui
    def breakdown_element_3_imgs() -> ui.TagList:
        return elig_char_breakdown().ui_imgs_in_section("element_3")

    @render.text
    def breakdown_op_text() -> str:
        count = elig_char_breakdown().n_chars_in_section("op")
        return f"{count} from Opening Characters"

    @render.ui
    def breakdown_op_imgs() -> ui.TagList:
        return elig_char_breakdown().ui_imgs_in_section("op")

    @render.text
    def breakdown_special_invite_text() -> str:
        count = elig_char_breakdown().n_chars_in_section("special_invites")
        return f"{count} from Special Invitations"

    @render.ui
    def breakdown_special_invite_imgs() -> ui.TagList:
        return elig_char_breakdown().ui_imgs_in_section("special_invites")

    @render.text
    def breakdown_traveler_text() -> str:
        count = elig_char_breakdown().n_chars_in_section("traveler")
        cluding = "including" if input.include_traveler() else "excluding"
        return f"{count} from {cluding} {input.traveler_name()}"

    @render.ui
    def breakdown_traveler_imgs() -> ui.TagList:
        return elig_char_breakdown().ui_imgs_in_section("traveler")


app = App(app_ui, server)
