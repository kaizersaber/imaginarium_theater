from shiny import ui, reactive, App, render
from datetime import datetime
import json

import load_data
from season import Season

app_ui = ui.page_fluid(
    ui.input_dark_mode(),
    ui.tags.link(
        rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Newsreader"
    ),
    ui.tags.style("body { font-family: 'Newsreader'}"),
    ui.panel_title("Imaginarium Theater"),
    ui.input_select(
        id="selected_season",
        label="",
        choices=load_data.season_labels(),
        selected=datetime.today().strftime("%B %Y"),
        width="170px",
    ),
    ui.p(),
    ui.panel_title("Alternate Cast Elements"),
    ui.output_text(id="selected_season_alt_cast_elements"),
    ui.p(),
    ui.panel_title("Opening Characters"),
    ui.output_text(id="selected_season_op_characters"),
    ui.p(),
    ui.panel_title("Special Invitations"),
    ui.output_text(id="selected_season_special_invites"),
    ui.p(),
    ui.panel_title("My Character Inventory"),
    ui.input_file(
        id="import_inventory",
        label="",
        button_label="Import from .json",
        accept=".json",
    ),
    ui.input_checkbox(
        id="include_traveler",
        label="Include Traveler?",
        value=True,
    ),
    ui.input_selectize(
        id="character_inventory",
        label="Type in box to search for character names",
        choices=load_data.character_names(),
        multiple=True,
    ),
    ui.help_text("Remember that a character must be level 70+ to be used!"),
    ui.p(),
    ui.download_button(id="export_inventory", label="Export to .json"),
    ui.p(),
    ui.panel_title("Result"),
)


def server(input, output, session):

    @render.text
    def selected_season_alt_cast_elements():
        return str(selected_season().alt_cast_elements)

    @render.text
    def selected_season_op_characters():
        return str(selected_season().op_characters)

    @render.text
    def selected_season_special_invites():
        return str(selected_season().special_invites)

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
        inventory = list(input.character_inventory())
        if input.include_traveler:
            inventory += ["Traveler"]
        yield json.dumps(inventory).encode("utf-8")


app = App(app_ui, server)
