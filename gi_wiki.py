import requests
import re
import pandas as pd
from bs4 import BeautifulSoup, element
from load_data import file_path, GI_WIKI_IMG_PATH
from timer import PerfProcTimer

GI_WIKI_URL = "https://genshin-impact.fandom.com/wiki/Characters"


def write_characters_to_csv(file_name: str) -> pd.DataFrame:
    timer = PerfProcTimer("Pulling character information from Genshin Impact Wiki...")
    characters = scrape_character_page()
    characters.to_csv(file_path(file_name), index=False)
    timer.end(f"Character information written to {file_name}")
    return characters


def scrape_character_page() -> pd.DataFrame:
    response = requests.get(GI_WIKI_URL)
    character_page = BeautifulSoup(response.text, "html.parser")
    character_tables = character_page.find_all(
        "table", class_="article-table sortable alternating-colors-table"
    )
    character_df = (
        pd.concat([_scrape_character_table(table) for table in character_tables])
        .sort_values("character")
        .reset_index(drop=True)
    )

    return _remove_traveler_dainsleif_from(character_df)


def _scrape_character_table(table: element.ResultSet) -> pd.DataFrame:
    character_df = pd.DataFrame(
        {
            "character": _scrape_characters_from(table),
            "element": _scrape_elements_from(table),
            "img_path": _scrape_img_paths_from(table),
        }
    )
    return character_df


def _scrape_characters_from(table: element.ResultSet) -> list[str]:
    characters = [
        td.find("a").attrs["title"]
        for td in [tr.find("td") for tr in table.find_all("tr")][1:]
    ]
    return characters


def _scrape_elements_from(table: element.ResultSet) -> list[str]:
    element_tags = [
        td[3].find("a") for td in [tr.find_all("td") for tr in table.find_all("tr")][1:]
    ]
    elements = [
        t.attrs["title"] if t is not None and t.has_attr("title") else "None"
        for t in element_tags
    ]
    return elements


def _scrape_img_paths_from(table: element.ResultSet) -> list[str]:
    pattern = f"{GI_WIKI_IMG_PATH}(.*?)/revision"
    img_paths = [
        re.findall(pattern, td.find("img").attrs["data-src"])[0]
        for td in [tr.find("td") for tr in table.find_all("tr")][1:]
    ]
    return img_paths


def _remove_traveler_dainsleif_from(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[~df["character"].isin(["Traveler", "Dainsleif"])]
