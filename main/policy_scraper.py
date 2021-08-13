import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

#launch Firefox driver
driver = webdriver.Firefox()

#handling websites with dynamically-loaded content 
driver.implicitly_wait(10)


def get_policy(browser, url): 
    '''
    This function returns a privacy policy in text format, from a given website url.
    '''

    #access a given url and handle exception if the url cannot be accesed
    try:
        browser.get(url) 
    except:
        print(f"Error: Something went wrong loading website {url}")
        return ""

    #look for anchor tags and href attributes containing the privacy keywords
    try:
        #find elements that meet the XPath Selector rules specified in brackets
        privacy_tags = browser.find_elements_by_xpath(f"//a[contains(@href, '{privacy_lower_case}')] | //a[contains(@href, '{privacy_upper_case}')] | //a[contains(.,'{privacy_lower_case}')] | //a[contains(.,'{privacy_upper_case}')]")
    except Exception as e:
        print(e, f"Error: MarionetteCommands")
        return ""
    
    #print a message if there are more than one tag meeting the XPath Selector rules 
    if len(privacy_tags) > 1:
        print(f"Note: Several privacy tags found for {url}")
    #print an error message and return statement if there are no tags meeting with XPath Selector rules
    elif len(privacy_tags) == 0:
        print(f"Error: No privacy tag found for {url}")
        return ""

    #dealing with StaleElementReferenceException  
    try:
        selected_tag = score_privacy_tags(privacy_tags)
        policy_link = selected_tag.get_attribute("href")       
    except Exception as e:
        print(e, url, f"Error: Stale Element")
        return ""

    #get policy link and deal with exception when url to policy page cannot be found 
    try: 
        browser.get(policy_link)
    except Exception as e: 
        print(e, f"Error: Something went wrong searching for the privacy page link on {url}")
        return ""

    #get page source from the privacy page
    try:
        page_source = browser.page_source
    except: 
        print(f"Error: No page source in privacy page of {url}")

    #apply the clean_policy() function to page_source and store it in policy_text
    policy_text = clean_policy(page_source)

    #add the clean policy_text to a text file in the policies directory
    file = open(f"policies/{url.split('www.')[1]}.txt", "w")
    file.write(policy_text)
    file.close()
    
    return policy_text


def score_privacy_tags(tags):
    '''
    Returns the most likely tag with the privacy policy
    '''

    score = [0] * len(tags)

    #increase or decrease a tag's score based on a set of conditions
    for i, tag in enumerate(tags):
        if tag.get_attribute("href") == None:
            score[i] = -100
            continue
        for st in ['privacy', 'Privacy']:
            if st in tag.get_attribute("href"):
                score[i] += 50

    best_index = 0

    #return tag with the highest score
    for i in range(len(score)):
        if score[i] > best_index:
            best_index = i
    return tags[i]


def clean_policy(policy_text):
    '''
    Clean data in policy text
    '''
    #prepare the html file by passing it in the BeautifulSoup constructor.
    soup = BeautifulSoup(policy_text, features="html.parser")
    
    #destroy all script and style elements
    #Method: take all data from HTML and remove <script> and <style> (blacklist)
    #Alternative: take all <p> <h1> <h...> <div> (whitelist) Might not work :(
    for tag in soup(["script", "style"]):
        tag.decompose()

    #get text (multi-line string variable)
    policy_text = soup.get_text()
    
    #break into lines and remove leading and trailing space on each (list of strings 1: per line)
    lines = policy_text.splitlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
  
    #break multi-headlines into a line each
    chunks = []
    for l in lines:
	    for s in l.split("  "):
		    chunks.append(s.strip())

    #drop blank lines
    not_blank = []
    for l in chunks:
	    if l != "":
		    not_blank.append(l)

    merged_text = '\n'.join(not_blank)

    return merged_text


##### MAIN #####

#indicate language of the input websites
website_language = 'English'

#set language keywords 
if website_language == 'English': 
    privacy_lower_case = 'privacy'
    privacy_upper_case = 'Privacy'

#input list of website URLs
url_file = 'url_list.csv'

#getting input list from "url_list.csv" and adding "https://www" in front of each element
url_list = pd.read_csv(url_file)['URL']

#run get_policy function on each URL in the input list of URLs
for url in url_list.values[1414:]:
    print(f"Getting policy for {url}")
    policy = get_policy(driver, url) 


driver.close()