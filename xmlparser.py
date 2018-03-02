"""
NASS CIREN provides an XML format of their case viewer. 
This script will provide functions and steps on parsing the data.

See example: https://crashviewer.nhtsa.dot.gov/nass-sci/CaseForm.aspx?GetXML&caseid=824229459&year=&transform=0&docInfo=0
"""

import requests
from xml.etree import ElementTree

def Example(verbose=False):
    CaseID = '824229459'
    url = buildURL(CaseID)
    xmlobject = getXML(url)
    if verbose:
        showXMLTree(xmlobject)
    return xmlobject


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

def showXMLTree(xmlobject, deep = 3):
    for child in xmlobject:
        print(child.tag)
        if deep > 1:
            for subchild in child:
                print("--", subchild.tag)
                if deep >2:
                    for subsub in subchild:
                        print('  --', subsub.tag)
    return None



class CaseViewer():
    
    def __init__(self, xmlobject, verbose=True):
        self.xmlobject = xmlobject
        self.verbose = verbose
    
    def get_vehicles(self):
        CaseForm = self.xmlobject.find('CaseForm')
        Vehicles = CaseForm.find('Vehicles')
        NumberVehicles = Vehicles.find('NumberVehicles')
        if self.verbose:
            print('Number of Vehicles', NumberVehicles)
        return Vehicles


def xml2dict(xmlobject, duplicate_tags = 'VehicleNumber'):
    """
    Convert XML to dict.
    Note some XML fields may have duplicate tags so data would be overwritten.
    This can be avoided by specifying `duplicate_tags` with the tag value to append
    the tag name with. For example, here we would specify `duplicate_tags = 'VehicleNumber'`
    <Vehicles>
        <VehicleSum VehicleNumber="1">
            <Year value="2001" sasCode="2001">2001</Year>
            <Make value="37" sasCode="37 ">HONDA</Make>
        </VehicleSum>
        <VehicleSum VehicleNumber="2">
            <Year value="2008" sasCode="2008">2008</Year>
            <Make value="37" sasCode="37 ">HONDA</Make>
        </VehicleSum>
    </Vehicles>
    """
    children = xmlobject.getchildren()
    n = len(children)
    if n == 0:
        return xmlobject.text
    else:
        stuff = dict()
        for i, child in enumerate(children, 1):
            addendum = child.get(duplicate_tags, '')
            key = child.tag + addendum
            stuff[key] = xml2dict(child, duplicate_tags)
        return stuff
    

def replace_none(x, replacement=''):
    "Replace `None` with `replacement`"
    if x is None:
        return replacement
    


class XML2Series():
    
    def __init__(self, xml_data):
        self.xml_data = xml_data
    
    
