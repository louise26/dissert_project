import pandas as pd 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

comp_name = 'Microsoft'

def load_data(comp_name):
    
   # gets url of comp name
    comp_dataset = pd.read_csv('websites/UKretailers.csv', sep=',')

    comp_website = comp_dataset[comp_dataset['Company name']==comp_name]['Website URL'].values[0]

    return comp_website

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get("https://Live.com")

buttons = driver.find_elements_by_xpath("//a[contains(@href, 'privacy')] | //a[contains(@href, 'Privacy')] | //a[contains(.,'privacy')] | //a[contains(.,'Privacy')]")

print(len(buttons))
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
file = open("microsoft_privacy1.txt", "w")
file.write(text)
file.close()

driver.close()