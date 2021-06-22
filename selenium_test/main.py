from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get("https://www.thetrainline.com")

buttons = driver.find_elements_by_xpath("//a[contains(@href, 'privacy')]")
policy_link = buttons[0].get_attribute("href")
print(policy_link)
driver.get(policy_link)
page_source = driver.page_source
soup = BeautifulSoup(page_source, features="html.parser")

# # kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# # get text
text = soup.get_text()

# # # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # # drop blank lines
# text_sanitized = '\n'.join(chunk for chunk in chunks if chunk)

#print(text)
print(text)

#add text to file
file = open("trainline_privacy1.txt", "w")
file.write(text)
file.close()

driver.close()