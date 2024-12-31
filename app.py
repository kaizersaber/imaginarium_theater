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
            ),
            ui.input_checkbox(
                id="include_traveler",
                label="Include Traveler?",
                value=True,
            ),
            ui.input_selectize(
                id="traveler_name",
                label="",
                choices=["Aether", "Lumine"],
                width="150px",
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
        ui.p(),
        ui.output_text(id="eligible_characters_text"),
        ui.div(
            ui.output_ui(id="eligible_characters_imgs"),
        ),
        ui.help_text(
            "Note that the above list will include opening characters that you may not currently have"
        ),
        ui.p(),
        ui.p("Made by xSaberFaye"),
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
            + datetime.today().date().strftime("%Y_%m_%d")
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

    @reactive.effect()
    def import_inventory():
        file = input.import_inventory()
        if file is not None:
            with open(file[0]["datapath"], "r") as f:
                inventory = json.load(f)
            ui_update_inventory(ui, inventory)

    @render.text
    def difficulty_text() -> str:
        season = selected_season()
        date = season.date.strftime("%B %Y")
        count = season.count_elig_characters_in(character_inventory())
        difficulty = season.highest_tier(count)
        if difficulty == "None":
            return f"You do not have enough characters to participate in the {date} season."
        else:
            return f"The highest difficulty you can challenge for the {date} season is {difficulty}."

    @render.text
    def eligible_characters_text() -> str:
        count = selected_season().count_elig_characters_in(character_inventory())
        return f"You have {count} eligible characters for this season:"

    @render.ui
    def eligible_characters_imgs() -> ui.TagList:
        selected_imgs = selected_season().get_elig_character_imgs_in(
            character_inventory(), input.traveler_name()
        )
        return ui_imgs(selected_imgs, width="50px")


app = App(app_ui, server)
