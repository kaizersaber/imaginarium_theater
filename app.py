from shiny.express import render, input
from shiny import ui

ui.panel_title("Imaginarium Theater Counter")


@render.text
def text():
    return "Hello World"
