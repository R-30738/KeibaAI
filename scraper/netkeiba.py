import io
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_html(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/150.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
        "Referer": "https://db.netkeiba.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url, timeout=20)
    response.raise_for_status()

    return response.content.decode("euc-jp", errors="replace")


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


def get_horse_result(horse_id):
    url = f"https://db.netkeiba.com/horse/ajax_horse_results.html?id={horse_id}"

    html = get_html(url)

    df = pd.read_html(StringIO(html))[0]

    columns = [
        "日付",
        "レース名",
        "着 順",
        "騎手",
        "斤 量",
        "距離",
        "馬 場",
        "タイム",
        "着差",
        "通過",
        "ペース",
        "上り",
        "馬体重",
        "人 気",
        "オ ッ ズ",
        "賞金",
    ]

    return df[columns]