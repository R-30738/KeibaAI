import io
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


def get_soup(url):
    html = get_html(url)
    return BeautifulSoup(html, "lxml")


def get_tables(url):
    html = get_html(url)
    return pd.read_html(io.StringIO(html))


def get_race_result(race_id):
    url = f"https://db.netkeiba.com/race/{race_id}/"
    tables = get_tables(url)
    return tables[0]


def get_shutuba(race_id):
    url = f"https://race.netkeiba.com/race/shutuba.html?race_id={race_id}"
    tables = get_tables(url)
    return tables[0]


def get_horse_list(race_id):
    url = f"https://race.netkeiba.com/race/shutuba.html?race_id={race_id}"
    soup = get_soup(url)

    horses = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "db.netkeiba.com/horse/" not in href:
            continue

        m = re.search(r"/horse/(\d+)", href)
        if not m:
            continue

        horse_id = m.group(1)
        horse_name = a.text.strip()

        if not horse_name:
            continue

        if horse_id in seen:
            continue

        seen.add(horse_id)

        horses.append({
            "horse_id": horse_id,
            "horse_name": horse_name
        })

    return horses