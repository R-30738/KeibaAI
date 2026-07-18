import io
import requests
import pandas as pd
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