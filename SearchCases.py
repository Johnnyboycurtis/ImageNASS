from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


CHROMEDRIVER = "./chromedriver"

browser = webdriver.Chrome(CHROMEDRIVER)

browser.get('https://www-nass.nhtsa.dot.gov/nass/cds/SearchForm.aspx')


elem = browser.find_element_by_name('SearchImageButtonTop')  # Find the search box
elem.send_keys(Keys.RETURN)

html = browser.page_source

soup = BeautifulSoup(html)
for tag in soup.find_all('title'):
    print(tag.text)

browser.quit()



