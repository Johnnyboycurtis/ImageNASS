"""
Requests images from NASS Crash Viewer
"""

import os
import xmlparser as xp
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import itertools as it





class CrashViewerImageRequest():
    def __init__(self, CaseID, directory, XMLData=None):
        """
        Builds URLs to images in NHTSA Crash Viewer
        """
        self.CaseID = CaseID ## iterable
        self.directory = directory
        self.URL = self.CrashViewerURL() ## URL to Case Viewer
        if XMLData:
            self.XMLData = XMLData

    
    def CrashViewerURL(self, return_ = False):
        '''
        Generate Crash Viewer URL
        '''
        URL = dict()
        for caseid in self.CaseID:
            url_full = xp.buildURL(caseid)
            URL[caseid] = url_full
        self.URL = URL
        if return_:
            return URL
    
    def getXML(self, return_=False, progress_bar=True):
        URL = self.URL
        XMLData = dict()
        URL_items = URL.items()
        if progress_bar:
            URL_items = tqdm(URL_items)
        for caseid, url in URL_items:
            xmlobject = xp.getXML(url)
            XMLData[caseid] = xmlobject
        if return_:
            return XMLData
        else:
            self.XMLData = XMLData

            
        
    
    def get_img_url(self, return_=False, progress_bar=True):
        '''
        Extract image URLs from XML data. 
        If `store = True`, saves XML data to self.XMLData
        If `return_ = True`, returns dict of image URL paths
        '''
        URL = self.URL
        XMLData = self.XMLData
        case_img = dict()
        for caseid, xmlobject in XMLData.items():
            url_paths = _get_image_paths(xmlobject) ## returns list
            case_img[caseid] = url_paths 
        self.img_url_path = case_img
        if return_:
            return case_img
    
    
    def parallel_images(self, progress_bar=True, save_results=True, results_file='CrashViewerResults.txt'):
        '''
        PARALLEL Request Images
        '''
        directory = self.directory
        
        Args = []
        URLDict = self.URL
        img_url_path = self.img_url_path
        for caseid, url in img_url_path.items():
            main_url = URLDict[caseid]
            img_info = img_url_path[caseid] ## caseid, vehicle, category, desc, ext, img_url
            _async_requests(caseid, main_url, img_info, directory)
            results_file = os.path.join(directory, results_file)
            with open(results_file, 'a+') as myfile:
                for line in img_info:
                    caseid, vehicle, category, desc, ext, img_url = line
                    image_name = '_'.join([caseid, vehicle, category, desc, ext])
                    image_name = image_name.replace('/', '-')
                    image_path = os.path.join(directory, image_name)
                    line = list(line)
                    line.append(image_path)
                    line.append(main_url)
                    try:
                        line = '|'.join(line)
                        myfile.write(line + '\n')
                    except TypeError:
                        print(line)
                        break


from concurrent.futures import ProcessPoolExecutor
from requests_futures.sessions import FuturesSession

def _async_requests(caseid, main_url, img_info, directory):
    my_session = requests.Session()
    sesh = FuturesSession(max_workers=6, session=my_session)
    #sesh = FuturesSession(executor=ProcessPoolExecutor(max_workers=10), session=my_session) ## does not work!!
    source = sesh.get(main_url) ## cache the session
    #del source ## delete this as unneccesary
    ## first make directory
    path = os.path.join(directory, str(caseid))
    if not os.path.exists(path):
        os.makedirs(path)

    Responses = []
    for caseid, vehicle, category, desc, ext, img_url in img_info:
        ## create image name
        image_name = '_'.join([caseid, vehicle, category, desc, ext])
        image_name = image_name.replace('/', '-')
        image_path = os.path.join(path, image_name)
        pull_image = sesh.get(img_url, stream=True)
        #Responses.append((image_path, pull_image))

    #for image_path, pull_image in Responses:
        response = pull_image.result()
        
        with open(image_path, "wb+") as myfile:
            myfile.write(response.content)



def _get_image_paths(xmlobject):
    url_path = 'https://crashviewer.nhtsa.dot.gov/nass-cds/GetBinary.aspx?Image&ImageID={}&CaseID={}&Version={}'
    CaseViewer = xp.CaseViewer(xmlobject)
    CaseID = CaseViewer.CaseID
    imgform = CaseViewer.IMGForm
    vehicles = imgform.findall('Vehicle')
    url_paths = list()
    for v in vehicles:
        ## for each vehicle, get tags
        vehicle_number = v.get('VehicleNumber')
        vehicle = '-'.join([v.tag, vehicle_number])
        tags = v.getchildren()
        for t in tags:
            ## for each img angle, e.g. front, back, backleft
            images = t.getchildren()
            for i in images:
                ## for each image
                ext = '.' + i.get('ext')
                desc = i.get('desc')
                version = i.get('version')
                imgid = i.text
                url_ = url_path.format(imgid, CaseID, version)
                url_paths.append((CaseID, vehicle, t.tag, desc, ext, url_))
    return url_paths
                    
                    
                    
                    
        
        
def flattenList(data):
    results = []
    for rec in data:
        if isinstance(rec, list):
            results += rec
            results = flattenList(results)
        else:
            results.append(rec)
    return results
