import pandas as pd
import subprocess
import time


def get_api_data(country_list): 
    '''
    makes API requests to Alexa, and store results in site_data
    '''

    start_point = 0
    range_ = range(1,501,100)
    for s in range_:
        options = f"\"&Count=100&Output=json&Start={start_point}&ResponseGroup=Country\""
        with open(f"websites_data/site_data_{s}.json", 'w') as f:
            command = f"python3 websites_data/topsites.py --key=KM19IsQpxiaSfQcBBcW431zop23rUEHq3hCbLpiA --action=TopSites --options {options} --country={country_list}"
            subprocess.Popen(command, shell=True, stdout=f)

        start_point += 100


###
def get_url_list():

    files = [pd.read_json(f'websites_data/site_data_{r}.json') for r in range(1,501,100)]

    site_urls = []

    for file in files:
        a_dict = file.loc['Results'].values[0]
        site_urls.extend([json_elem['DataUrl'] for json_elem in a_dict['Result']['Alexa']['TopSites']['Country']['Sites']['Site']])

    site_urls = pd.Series(site_urls)
    site_urls.name = 'URL'
    site_urls = site_urls.apply(lambda x: "https://www."+x)
    site_urls.to_csv('url_list.csv', index=False)
    

country_list = 'GB'

get_api_data(country_list)

time.sleep(5)

get_url_list()