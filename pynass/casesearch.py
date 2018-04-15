import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
#from sys import platform
#import os

class SearchNASS():
    def __init__(self, chromedriver='/home/jn107154/Documents/chromedriver'):
	    self.chromedriver = chromedriver
            
    def Search(self, PlaneOfImpact, Year, MinVeh, MaxVeh, Month='All', Make='All', Model='All', PlaneSubSection='All'):
        browser = webdriver.Chrome(self.chromedriver)
        browser.get('https://crashviewer.nhtsa.dot.gov/LegacyCDS/Search')
        browser.find_element_by_xpath("//select[@name='ddlMake']/option[text()='{}']".format(Make)).click()
        browser.find_element_by_xpath("//select[@name='ddlModel']/option[text()='{}']".format(Model)).click()
        browser.find_element_by_xpath("//select[@name='ddlPrimaryDamage']/option[text()='{}']".format(PlaneOfImpact)).click()
        browser.find_element_by_xpath("//select[@name='lSecondaryDamage']/option[text()='{}']".format(PlaneSubSection)).click()
        browser.find_element_by_xpath("//select[@name='ddlYear']/option[text()='{}']".format(Year)).click()
        browser.find_element_by_xpath("//select[@name='ddlMonth']/option[text()='{}']".format(Month)).click()
        browser.find_element_by_xpath("//select[@name='ddlMinVeh']/option[text()='{}']".format(MinVeh)).click()
        browser.find_element_by_xpath("//select[@name='ddlMaxVeh']/option[text()='{}']".format(MaxVeh)).click()
        
        elem = browser.find_element_by_id('btnSubmit1')  # Find the search box
        elem.send_keys(Keys.RETURN)

        CaseIDResults = dict()

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
                href = x['href']
                caseid =  href.split('=')[-1]
                CaseIDResults[caseid] = href

            try:
                next_page = browser.find_element_by_id("lNext")
                next_page.click()
            except selenium.common.exceptions.ElementNotVisibleException:
                break
                    
        return CaseIDResults


def Example():
    """
    tmp = SearchNASS()
    results = tmp.Search(PlaneOfImpact='Front', Year='2015', Month='Jun')
    return results
    """
    tmp = SearchNASS()
    results = tmp.Search(PlaneOfImpact='Front', Year='2015', Month='Jan', MinVeh=2, MaxVeh=2)
    return results

if __name__ ==  '__main__':
    results = Example()
    print(results)