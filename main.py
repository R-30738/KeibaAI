from scraper.netkeiba import get_horse_list

race_id = input("レースIDを入力してください：")

horses = get_horse_list(race_id)

for horse in horses:
    print(f"{horse['horse_name']} : {horse['horse_id']}")