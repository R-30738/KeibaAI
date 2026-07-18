from scraper.netkeiba import get_shutuba

race_id = input("レースIDを入力してください：")

df = get_shutuba(race_id)

print(df.head())