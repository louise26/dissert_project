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

def score_buttons(buttons):
    '''Returns the most likely button with the privacy policy'''
    score = [0] * len(buttons)
    for i, button in enumerate(buttons):
        if button.get_attribute("href") == None:
            score[i] = -100
            continue
        if "policy" in button.get_attribute("href"):
            score[i] += 50
        # TODO if the word "policy can be found in the a body than score += 30"
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
        print(f"Something went wrong loading website {url}")
        return ""

    #href link or <a> tag contains the word privacy
    privacy_buttons = browser.find_elements_by_xpath("//a[contains(@href, 'privacy')] | //a[contains(@href, 'Privacy')] | //a[contains(.,'privacy')] | //a[contains(.,'Privacy')]")
    #print message if there is more or less than one privacy button 
    if len(privacy_buttons) > 1:
        print(f"Scrapper has found several privacy buttons for {url}")
    elif len(privacy_buttons) == 0:
        print(f"Error: No buttons found for {url}")
        return ""
    choosen_button = score_buttons(privacy_buttons)
   
    policy_link = choosen_button.get_attribute("href")

   #get policy link and deal with exception when there are more than one policy link 
    try: 
        browser.get(policy_link)
    except: 
        print(f"Something went searching for the privacy page link on {url}")
        return ""
    
    # If the word "policy" not in `policy_link` then:
    # From policy_link page check AGAIN for a tags with potential links
    # Going to a "policy" page

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

for url in url_list[29:]:
    print(f"Getting policy for {url}")
    policy = get_policy(driver, url) 


driver.close()