import pandas as pd
import subprocess
import time


def get_api_data(country_list): 
    '''
    This function makes API requests to Alexa, and store results in json files, in the websites_data directory. 
    '''

    start_point = 0
    request_range = range(1,num_websites+1,100)
    
    #for each API request, execute topsites.py with the options defined in the options variable, and store results in json files
    for s in request_range:
        options = f"\"&Count=100&Output=json&Start={start_point}&ResponseGroup=Country\""
        with open(f"websites_data/site_data_{s}.json", 'w') as f:
            command = f"python3 websites_data/topsites.py --key=KM19IsQpxiaSfQcBBcW431zop23rUEHq3hCbLpiA --action=TopSites --options {options} --country={country_list}"
            subprocess.Popen(command, shell=True, stdout=f)

        #indent start_point by 100 for next request
        start_point += 100


def get_url_list():
    '''
    This function extract URLs from json files and creates a list of valid URLs, which is stored in a CSV file. 
    '''

    #read json files in websites_data and store them in pandas Series called "files"
    files = [pd.read_json(f'websites_data/site_data_{r}.json') for r in range(1,num_websites+1,100)]

    #create empty list
    site_urls = []

    #in each json file, search for element 'DataURL', and store these elements in the site_urls list
    for file in files:
        dict = file.loc['Results'].values[0]
        site_urls.extend([json_elem['DataUrl'] for json_elem in dict['Result']['Alexa']['TopSites']['Country']['Sites']['Site']])

    #convert site_urls list to a Pandas Series
    site_urls = pd.Series(site_urls)
    site_urls.name = 'URL'
    #add "https://www." prefix to make url valid 
    site_urls = site_urls.apply(lambda x: "https://www."+x)
    #add list of urls to a csv file
    site_urls.to_csv('url_list.csv', index=False)

####### MAIN #######

#choose country to get topsites from using country code
country_list = 'GB'

#choose how many websites' URLS we want to collect (max = 1603)
num_websites = 500

get_api_data(country_list)

#make sure that get_api_data is executed before calling get_url_list 
time.sleep(5)

get_url_list()
