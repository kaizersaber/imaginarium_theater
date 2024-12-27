from shiny import ui, reactive, App, render
from datetime import datetime
import json

import load_data
from season import Season
from ui_elements import imgs_from_paths

app_ui = ui.page_fluid(
    ui.head_content(ui.tags.title("Imaginarium Theater")),
    ui.input_dark_mode(),
    ui.tags.link(
        rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Newsreader"
    ),
    ui.tags.style("body { font-family: 'Newsreader'}"),
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
        ui.panel_title("My Character Inventory"),
        ui.div(
            ui.input_file(
                id="import_inventory",
                label="You can import a previously exported inventory here:",
                button_label="Import from .json",
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
        ui.p(),
        ui.input_selectize(
            id="character_inventory",
            label="Type in box to search for character names",
            choices=load_data.character_names(),
            multiple=True,
            width="100%",
        ),
        ui.help_text("Remember that a character must be level 70+ to be used!"),
        ui.div(ui.download_button(id="export_inventory", label="Export to .json")),
        ui.p(),
        ui.panel_title("Calculator Results"),
        ui.output_text(id="difficulty_text"),
        ui.p(),
        ui.output_text(id="eligible_characters_text"),
        ui.div(
            ui.output_ui(id="eligible_characters_imgs"),
        ),
        ui.p(),
        ui.p("Made by xSaberFaye"),
        align="center",
    ),
)


def server(input, output, session):
    @render.ui
    def selected_season_alt_cast_elements():
        selected_img_paths = selected_season().get_element_img_paths()
        return imgs_from_paths(selected_img_paths, width="50px")

    @render.ui
    def selected_season_op_characters():
        selected_img_paths = selected_season().get_op_character_img_paths()
        return imgs_from_paths(selected_img_paths, width="50px")

    @render.ui
    def selected_season_special_invites():
        selected_img_paths = selected_season().get_special_invite_img_paths()
        return imgs_from_paths(selected_img_paths, width="50px")

    @reactive.calc
    def selected_season():
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
    def character_inventory():
        inventory = list(input.character_inventory())
        if input.include_traveler():
            inventory += ["Traveler"]
        return inventory

    @reactive.effect()
    def import_inventory():
        inventory = input.import_inventory()
        if inventory is not None:
            with open(inventory[0]["datapath"], "r") as f:
                inventory = json.load(f)
            traveler_in_inv = "Traveler" in inventory
            ui.update_checkbox(id="include_traveler", value=traveler_in_inv)
            if traveler_in_inv:
                inventory.remove("Traveler")
            ui.update_selectize(id="character_inventory", selected=inventory)

    @render.text
    def difficulty_text():
        season = selected_season()
        date = season.date.strftime("%B %Y")
        count = season.count_elig_characters_in(character_inventory())
        difficulty = season.highest_difficulty(count)
        if difficulty == "None":
            return f"You do not have enough characters to participate in the {date} season."
        else:
            return f"The highest difficulty you can challenge for the {date} season is {difficulty}."

    @render.text
    def eligible_characters_text():
        count = selected_season().count_elig_characters_in(character_inventory())
        return f"You have {count} eligible characters for this season:"

    @render.ui
    def eligible_characters_imgs():
        selected_img_paths = selected_season().get_elig_character_imgs_in(
            character_inventory(), input.traveler_name()
        )
        return imgs_from_paths(selected_img_paths, width="50px")


app = App(app_ui, server)
