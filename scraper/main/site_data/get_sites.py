import pandas as pd
files = [pd.read_json(f'site_data_{r}.json') for r in range(1,501,100)]

site_urls = []

for file in files:
    a_dict = file.loc['Results'].values[0]
    site_urls.extend([json_thing['DataUrl'] for json_thing in a_dict['Result']['Alexa']['TopSites']['Country']['Sites']['Site']])

site_urls = pd.Series(site_urls)
site_urls.name = 'URL'
site_urls.to_csv('url_list.csv', index=False)