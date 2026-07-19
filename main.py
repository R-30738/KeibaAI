from scraper.netkeiba import get_horse_result

horse_id = "2022101193"

df = get_horse_result(horse_id)

print(df.columns)