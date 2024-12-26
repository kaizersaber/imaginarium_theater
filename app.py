from shiny.express import render, input
from shiny import ui, reactive
import data.load
from logic.season import Season

ui.input_dark_mode()

ui.tags.link(
    rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Newsreader"
)

ui.tags.style("body { font-family: 'Newsreader'}")

ui.panel_title("Imaginarium Theater")

ui.input_select(
    id="selected_season",
    label="",
    choices=data.load.season_labels(),
    width="170px",
)


@reactive.calc
def selected_season():
    return Season(input.selected_season())


ui.p()
ui.panel_title("Alternate Cast Elements")


@render.text
def selected_season_alt_cast_elements():
    return str(selected_season().alt_cast_elements)


ui.p()
ui.panel_title("Opening Characters")


@render.text
def selected_season_op_characters():
    return str(selected_season().op_characters)


ui.p()
ui.panel_title("Special Invitations")


@render.text
def selected_season_special_invites():
    return str(selected_season().special_invites)
