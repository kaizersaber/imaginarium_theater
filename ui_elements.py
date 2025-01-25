from shiny import ui
import load_data


def ui_breakdown() -> list:
    sections = [f"element_{i}" for i in [1, 2, 3]]
    sections += ["op", "special_invite", "traveler"]

    text_ids = [f"breakdown_{s}_text" for s in sections]
    img_ids = [f"breakdown_{s}_imgs" for s in sections]

    ui_columns = [
        ui.column(
            2,
            ui.output_text(id=text_id),
            ui.div(ui.output_ui(id=img_id)),
            style="padding:0px",
        )
        for text_id, img_id in zip(text_ids, img_ids)
    ]
    return ui.row(*ui_columns)


def ui_imgs(names_and_paths: tuple[str, str], width: str) -> ui.TagList:
    imgs = [
        ui.tooltip(ui.img(src=p, width=width), n, placement="bottom")
        for n, p in names_and_paths
    ]
    return ui.TagList(*imgs)


def ui_update_inventory(app_ui: ui, inventory: dict | list[str]):
    if "characters" in inventory:
        inventory = _convert_GOOD_to_list(inventory)

    traveler_in_inv = "Traveler" in inventory
    app_ui.update_checkbox(id="include_traveler", value=traveler_in_inv)
    if traveler_in_inv:
        inventory.remove("Traveler")
    app_ui.update_selectize(id="character_inventory", selected=inventory)


def _convert_GOOD_to_list(inventory_good: dict) -> list[str]:
    keys = [c["key"] for c in inventory_good["characters"] if c["level"] >= 70]
    inventory_list = [
        load_data.character_keys()[k] for k in keys if "Traveler" not in k
    ]

    traveler_in_inv = any(["Traveler" in k for k in keys])
    if traveler_in_inv:
        inventory_list += ["Traveler"]

    return inventory_list
