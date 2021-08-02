import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

driver = webdriver.Firefox()

def score_buttons(buttons):
    '''Returns the most likely button with the privacy policy'''
    score = [0] * len(buttons)
    for i, button in enumerate(buttons):
        if button.get_attribute("href") == None:
            score[i] = -100
            continue
        if "policy" in button.get_attribute("href"):
            score[i] += 50

    best_index = 0
    for i in range(len(score)):
        if score[i] > best_index:
            best_index = i
    return buttons[i]


def get_policy(browser, url): 
    '''Returns privacy policy from given website url'''

    #deal with exception if URL does not exist
    try:
        browser.get(url) 
    except:
        print(f"Error: Something went wrong loading website {url}")
        return ""


    #look for an href link or <a> tag containing the word 'privacy' or 'Privacy'
    privacy_buttons = browser.find_elements_by_xpath("//a[contains(@href, 'privacy')] | //a[contains(@href, 'Privacy')] | //a[contains(.,'privacy')] | //a[contains(.,'Privacy')]")
    print(len(privacy_buttons))
    
    #print message if there is more or less than one privacy button 
    if len(privacy_buttons) > 1:
        print(f"Note: Several privacy buttons found for {url}")
    elif len(privacy_buttons) == 0:
        print(f"Error: No privacy button found for {url}")
        return ""

    #dealing with StaleElementReferenceException  
    try:
        chosen_button = score_buttons(privacy_buttons)
        policy_link = chosen_button.get_attribute("href")       
    except Exception as e:
        print(e, url, f"Error: at chosen_button")
        return ""

    #get policy link and deal with exception when url to policy page cannot be found 
    try: 
        browser.get(policy_link)
    except: 
        print(f"Error: Something went wrong searching for the privacy page link on {url}")
        return ""

    # If the word "policy" not in `policy_link` then:
    # From policy_link page check AGAIN for a tags with potential links
    # Going to a "policy" page

    page_source = browser.page_source

    policy_text = clean_policy(page_source)

    #add text to file
    try: 
        file = open(f"policies/{url.split('www.')[1]}.txt", "w")
        file.write(policy_text)
        file.close()
    except: 
        print("Policy file has not been created")
        return ""
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

url_file = 'site_data/url_list.csv'

#Getting the 500 website list from file "url_list.csv" and adding "https://www" in front of all to find URL
url_list = pd.read_csv(url_file)['URL'].apply(lambda x: "https://www."+x)
print(url_list)

#for url in url_list.values[:5]:
for url in url_list:
    print(f"Getting policy for {url}")
    policy = get_policy(driver, url) 


driver.close()