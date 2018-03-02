"""
NASS CIREN provides an XML format of their case viewer. 
This script will provide functions and steps on parsing the data.

See example: https://crashviewer.nhtsa.dot.gov/nass-sci/CaseForm.aspx?GetXML&caseid=824229459&year=&transform=0&docInfo=0
"""

import requests
from xml.etree import ElementTree

CaseIDList = ['824229459' ]


def buildURL(CaseID):
    "Takes in CaseID string and returns a URL from which to obtain XML data"
    url = 'https://crashviewer.nhtsa.dot.gov/nass-sci/CaseForm.aspx?GetXML&caseid={}&year=&transform=0&docInfo=0'.format(CaseID)
    return url

def getXML(url):
    """
    Uses requests library to pull XML data as string then 
    parses it with xml.etree.ElementTree
    """
    result = requests.get(url)
    xmlresult = ElementTree.fromstring(result.text)
    return xmlresult






