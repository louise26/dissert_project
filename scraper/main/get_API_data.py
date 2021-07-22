import pandas as pd

country_list = ['GB']
start_point = 0
range_ = range(1,501,100)
for s in range_:
    !cd /Users/louisemoizan/Documents/dissert_project/scraper/main/site_data && python topsites.py --key=KM19IsQpxiaSfQcBBcW431zop23rUEHq3hCbLpiA --action=TopSites --options=f"&Count=100&Output=json&Start={start_point}&ResponseGroup=Country" --country=GB > site_data_{s}.json
    start_point += 100