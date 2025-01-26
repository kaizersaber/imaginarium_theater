from shiny import ui
import load_data


def ui_season_info() -> list:
    titles = [
        "Alternate Cast Elements",
        "Opening Characters",
        "Special Invitations",
    ]
    ids = [
        "selected_season_alt_cast_elements",
        "selected_season_op_characters",
        "selected_season_special_invites",
    ]
    ui_columns = [
        ui.column(
            4,
            ui.panel_title(title),
            ui.output_ui(id=id),
            align="center",
        )
        for title, id in zip(titles, ids)
    ]
    return ui.row(*ui_columns)


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


def ui_credits() -> list:
    text_link_urls = [
        [
            "Made by",
            "xSaberFaye",
            "https://www.youtube.com/@xsaberfaye",
        ],
        [
            " - Season information from",
            "HomDGCat Wiki",
            "https://homdgcat.wiki/gi/maze?lang=EN",
        ],
        [
            " - Image assets from",
            "Genshin Impact Wiki",
            "https://genshin-impact.fandom.com/wiki/Character/List",
        ],
        [
            " - View source code on",
            "Github",
            "https://github.com/kaizersaber/imaginarium_theater",
        ],
    ]
    credits = [
        part
        for text, link, url in text_link_urls
        for part in [
            f"{text} ",
            ui.tags.a(link, href=url, target="_blank"),
        ]
    ]
    return ui.p(*credits)


def ui_imgs(names_and_paths: tuple[str, str], width: str = "50px") -> ui.TagList:
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
