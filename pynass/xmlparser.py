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
        self.CaseForm = xmlobject.find('CaseForm')
        self.EMSForm = xmlobject.find('EMSForm')
        self.GeneralVehicleForms = xmlobject.find('GeneralVehicleForms')
        self.IMGForm = xmlobject.find('IMGForm')
        self.OccupantForms = xmlobject.find('OccupantForms')
        self.SciCaseForm = xmlobject.find('SciCaseForm')
        self.SafetyForms = xmlobject.find('SafetyForms')
        self.VehicleExteriorForms = xmlobject.find('VehicleExteriorForms')
        self.VehicleInteriorForms = xmlobject.find('VehicleInteriorForms')
    
    def get_vehicles(self, as_dict = False):
        """
        From Case Form get vehicle data
        """
        Vehicles = self.CaseForm.find('Vehicles')
        NumberVehicles = Vehicles.find('NumberVehicles')
        if self.verbose:
            print('Number of Vehicles', NumberVehicles)
        if as_dict:
            Vehicles = xml2dict(Vehicles)
        return Vehicles
    
    def get_events(self, as_dict = False):
        """
        From Case Form get events data
        """
        Events = self.CaseForm.find('Events')
        if as_dict:
            Events = xml2dict(Events)
        return Events
    
    def get_persons(self, as_dict = False):
        """
        From Case Form get persons data
        """
        Persons = self.CaseForm.find('Persons')
        if as_dict:
            Persons = xml2dict(Persons)
        return Persons
        


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
        for child in children:
            addendum = child.get(duplicate_tags, '')
            key = child.tag + addendum
            stuff[key] = xml2dict(child, duplicate_tags)
        return stuff
    

class XML2Pandas():
    
    def __init__(self, xml_data):
        """
        Takes an xml object and parses it to a dictionary in self.data
        Can return a pandas.Series or pandas.DataFrame object
        """
        self.xml_data = xml_data
        self.data = xml2dict(xml_data)

    def to_Series(self):
        return pd.Series(self.data)

    def to_DataFrame(self, transpose=True):
        df = pd.DataFrame(self.data)
        if transpose:
            return df.T
        else:
            return df

    
    
        
    
    
