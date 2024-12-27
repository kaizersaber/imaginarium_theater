from shiny import ui


def imgs_from_paths(paths: list[str], width):
    imgs = [ui.img(src=p, width=width) for p in paths]
    return ui.TagList(*imgs)


def ui_update_inventory(app_ui: ui, inventory: list[str]):
    traveler_in_inv = "Traveler" in inventory
    app_ui.update_checkbox(id="include_traveler", value=traveler_in_inv)
    if traveler_in_inv:
        inventory.remove("Traveler")
    app_ui.update_selectize(id="character_inventory", selected=inventory)
