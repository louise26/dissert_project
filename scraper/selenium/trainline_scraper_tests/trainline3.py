import pandas as pd 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

comp_name = 'Trainline'
comp_link = "https://www.thetrainline.com"


options = Options()
options.headless = True

def get_policy(browser, url): 
    '''Returns privacy policy from given website url'''

    driver = webdriver.Firefox(options=options)
    driver.get(comp_link)
    
    buttons = driver.find_elements_by_xpath("//a[contains(@href, 'privacy')]")
    policy_link = buttons[0].get_attribute("href")
    print(policy_link)
    driver.get(policy_link)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features="html.parser")
    
    #kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    
    #get text
    text = soup.get_text()
    
    #print(text)
    print(text)
    
    #add text to file
    file = open("trainline_privacy1.txt", "w")
    file.write(text)
    file.close()

driver.close()