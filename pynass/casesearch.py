import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from sys import platform
import os

class SearchNASS():
    def __init__(self, chromedriver='/home/jn107154/Documents/chromedriver'):
	    self.chromedriver = chromedriver
            
    def Search(self, PlaneOfImpact, Year, Month, PlaneSubSection='All'):
        browser = webdriver.Chrome(self.chromedriver)
        browser.get('https://crashviewer.nhtsa.dot.gov/LegacyCDS/Search')
        browser.find_element_by_xpath("//select[@name='ddlPrimaryDamage']/option[text()='{}']".format(PlaneOfImpact)).click()
        browser.find_element_by_xpath("//select[@name='lSecondaryDamage']/option[text()='{}']".format(PlaneSubSection)).click()
        browser.find_element_by_xpath("//select[@name='ddlYear']/option[text()='{}']".format(Year)).click()
        browser.find_element_by_xpath("//select[@name='ddlMonth']/option[text()='{}']".format(Month)).click()
        
        elem = browser.find_element_by_id('btnSubmit')  # Find the search box
        elem.send_keys(Keys.RETURN)

        CaseID = []

        while True:
            html = browser.page_source
            soup = BeautifulSoup(html)
            
            for tag in soup.find_all('title'):
                print(tag.text)
            lcasecount = soup.find('span', id = 'lCaseCount')
            print(lcasecount.text) ## print case count

            xtable,  = soup.find_all('table', class_="display table table-condensed table-striped table-hover")
            tr_tags = xtable.find_all('a', href = True)
            #print(tr_tags)
            
            for i,x in enumerate(tr_tags):
                #print(i, x)
                caseid =  x['href'].split('=')[-1]
                #print(i, x['href'])
                CaseID.append(caseid)
                #print(caseid)
                #break ## for testing!!
            try:
                next_page = browser.find_element_by_id("lNext")
                next_page.click()
            except selenium.common.exceptions.ElementNotVisibleException:
                break
                    
        return CaseID



tmp = SearchNASS()
results = tmp.Search(PlaneOfImpact='Front', Year='2015', Month='Jun')
print(results)

