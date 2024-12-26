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
    ui.output_ui(id="selected_season_elements_img"),
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
        width="100%",
    ),
    ui.help_text("Remember that a character must be level 70+ to be used!"),
    ui.p(),
    ui.download_button(id="export_inventory", label="Export to .json"),
    ui.p(),
    ui.panel_title("Calculator Results"),
    ui.output_text(id="difficulty_text"),
    ui.p(),
    ui.output_text(id="eligible_characters_text"),
)


def server(input, output, session):
    @render.ui
    def selected_season_elements_img():
        elements = load_data.elements()
        img_paths = [elements[e] for e in selected_season().alt_cast_elements]
        images = [ui.img(src=p, width="50px") for p in img_paths]
        return ui.TagList(*images)

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
        characters = selected_season().get_elig_characters_in(character_inventory())
        count = len(characters)
        return f"You have {count} eligible characters for this season: {str(sorted(characters))}"


app = App(app_ui, server)
