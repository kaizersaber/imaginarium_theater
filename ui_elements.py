from shiny import ui
from faicons import icon_svg
import load_data
import re

FONT_FAMILY = "Poppins"


def ui_season_info() -> list:
    titles = [
        "Alternate Cast Elements",
        "Opening Characters",
        "Special Invitations",
    ]
    sections = ["alt_cast_elements", "op_characters", "special_invites"]
    ids = [f"selected_season_{s}" for s in sections]
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
            "Data and assets from",
            "HomDGCat Wiki",
            "https://homdgcat.wiki/gi/maze?lang=EN",
        ],
        [
            " - Made by xSaberFaye",
            icon_svg("youtube"),
            "https://www.youtube.com/@xsaberfaye",
        ],
        ["", icon_svg("twitch"), "https://www.twitch.tv/xsaberfaye"],
        [
            "",
            icon_enka(),
            "https://enka.network/u/604534740/",
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


def icon_enka() -> ui.HTML:
    svg_html = f"""
    <svg viewBox="0 0 576 512" preserveAspectRatio="none" aria-hidden="true"
        role="img" class="fa"
        style="fill:currentColor;height:4em;width:4em;margin-left:auto;margin-right:0.2em;position:relative;vertical-align:-3.15em;overflow:visible;">
        <g transform="translate(0.000000,109.000000) scale(0.100000,-0.100000)">
            <path d="M535 910 c-54 -94 -96 -172 -94 -174 2 -2 32 -18 66 -35 l63 -31 13 22 c8 13 23 38 34 57 l20 33 35 -58 c20 -33 73 -124 118 -204 46 -80 85 -147 87 -149 4 -6 123 51 130 62 4 7 -337 608 -362 635 -9 10 -32 -22 -110 -158z"/>
            <path d="M195 324 c-94 -162 -171 -299 -173 -304 -2 -6 41 -10 110 -10 l113 1 41 72 c42 72 42 72 18 75 -13 2 -24 5 -24 7 0 1 50 89 111 195 61 105 109 193 107 195 -5 4 -127 65 -130 65 -2 -1 -79 -133 -173 -296z"/>
            <path d="M559 455 l-75 -76 77 -82 78 -82 80 80 81 80 -77 77 c-43 43 -80 78 -83 78 -3 0 -39 -34 -81 -75z"/>
            <path d="M1017 285 c-31 -17 -60 -34 -63 -37 -3 -4 6 -24 20 -47 l26 -41 -262 -2 -261 -3 -43 -73 -43 -72 436 0 435 0 -14 23 c-8 12 -47 79 -88 150 -40 70 -75 129 -79 131 -3 2 -32 -11 -64 -29z"/>
        </g>
    </svg>
    """
    return ui.HTML(svg_html)


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
