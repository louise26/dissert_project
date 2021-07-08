from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

#Get list of top 50 website names from Alexa and store the list on a txt file. 

driver = webdriver.Firefox()
website_database = "https://www.alexa.com/topsites/countries/GB"

def get_websites(browser, starting_point):
    '''Retrieves website links from starting point'''
    browser.get(starting_point)
    websites = browser.find_elements_by_xpath("//p/a")
    url_list = []
    for value in websites:
        url_list.append("https://" + value.text)

    return url_list

def get_policy(browser, url): 
    '''Returns privacy policy from given website url'''

    browser.get(url)
    
    privacy_button = browser.find_elements_by_xpath("//a[contains(@href, 'privacy')] | //a[contains(@href, 'Privacy')]")
    print(len(privacy_button) == 0) #DEBUGGING
    policy_link = privacy_button[0].get_attribute("href")#TODO review if several buttons are found
   
    browser.get(policy_link)
    page_source = browser.page_source

    policy_text = clean_policy(page_source)

    #add text to file
    file = open(f"{url.split('//')[1]}.txt", "w")
    file.write(policy_text)
    file.close()

    return policy_text

def clean_policy(policy_text):
    '''Clean data in policy text'''

    soup = BeautifulSoup(policy_text, features="html.parser")
    
    #kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    #get text
    policy_text = soup.get_text()
    
    #break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in policy_text.splitlines())
    #break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    #drop blank lines
    text_sanitized = '\n'.join(chunk for chunk in chunks if chunk)

    #return policy_text
    return text_sanitized


#MAIN#
url_list = get_websites(driver, website_database)
print(url_list)

for url in url_list[:25]:
    print(f"Getting policy for {url}")
    policy = get_policy(driver, url) 


driver.close()