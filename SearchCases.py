import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from sys import platform
import os

if platform == "linux":
    CHROMEDRIVER = "./chromedriver"
else:
    CHROMEDRIVER = os.environ.get('CHROMEDRIVER', None)
    print("Missing Chrome Driver")

browser = webdriver.Chrome(CHROMEDRIVER)

browser.get('https://www-nass.nhtsa.dot.gov/nass/cds/SearchForm.aspx')


##

#ddlmake = browser.find_element_by_id("ddlMake")
#browser.find_element_by_xpath("//select[@name='element_name']/option[text()='option_text']").click()
browser.find_element_by_xpath("//select[@name='ddlMake']/option[text()='HONDA']").click()
browser.find_element_by_xpath("//select[@name='ddlModel']/option[text()='CIVIC/CRX/DEL SOL']").click()
browser.find_element_by_xpath("//select[@name='ddlStartModelYear']/option[text()='2000']").click()
##



elem = browser.find_element_by_name('SearchImageButtonTop')  # Find the search box
elem.send_keys(Keys.RETURN)



"""
html = browser.page_source

soup = BeautifulSoup(html)
for tag in soup.find_all('title'):
    print(tag.text)


xtable,  = soup.find_all('table', id="ListTable")
#tr_tags = xtable.find_all('tr') ## each row is in a tr tag
tr_tags = xtable.find_all('a', href=True) ## directly obtain href tags
for i,x in enumerate(tr_tags):
    print(i, x)
    print(i, x['href'])
    print(i,x.text)
    break

try:
    next_page = browser.find_element_by_id("lNext")
    next_page.click()
except selenium.common.exceptions.NoSuchElementException:
    pass



html = browser.page_source

soup = BeautifulSoup(html)
for tag in soup.find_all('title'):
    print(tag.text)

xtable,  = soup.find_all('table', id="ListTable")
#tr_tags = xtable.find_all('tr') ## each row is in a tr tag
tr_tags = xtable.find_all('a', href=True) ## directly obtain href tags
for i,x in enumerate(tr_tags):
    print(i, x)
    print(i, x['href'])
    print(i,x.text)
    break
"""

while True:
    html = browser.page_source
    soup = BeautifulSoup(html)
    for tag in soup.find_all('title'):
        print(tag.text)
    lcasecount = soup.find('span', id = 'lCaseCount')
    xtable, = soup.find_all('table', id = 'ListTable')
    tr_tags = xtable.find_all('a', href = True)
    print(lcasecount.text)
    for i,x in enumerate(tr_tags):
        print(i, x)
        #print(i, x['href'])
        break
    try:
        next_page = browser.find_element_by_id("lNext")
        next_page.click()
    except selenium.common.exceptions.NoSuchElementException:
        break



browser.quit()



