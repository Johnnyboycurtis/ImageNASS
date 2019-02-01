#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 09:14:39 2018

@author: jn107154
"""


import os
import pynass.xmlparser as xp
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import xmlparser as xp
import pandas as pd

class CrashViewerImageRequest():
    def __init__(self, CaseID, directory, XMLData=None):
        """
        Builds URLs to images in NHTSA Crash Viewer
        """
        self.CaseID = CaseID ## iterable
        self.directory = directory
        self.URL = self.CrashViewerURL() ## URL to Case Viewer
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
    
    def get_xml(self, return_=False, progress_bar=True):
        URL = self.URL
        XMLData = dict()
        URL_items = URL.items()
        if progress_bar:
            URL_items = tqdm(URL_items)
        for caseid, url in URL_items:
            xmlobject = xp.getXML(url)
            XMLData[caseid] = xmlobject
        self.XMLData = XMLData
        if return_:
            return XMLData
    
    def get_img_url(self, return_=False, progress_bar=True):
        '''
        Extract image URLs from XML data. 
        If `store = True`, saves XML data to self.XMLData
        If `return_ = True`, returns dict of image URL paths
        '''
        URL = self.URL
        XMLData = self.XMLData
        case_img = dict()
        URL_items = URL.items()
        if progress_bar:
            URL_items = tqdm(URL_items)
        for caseid, url in URL_items:
            if self.XMLData == None:
                xmlobject = xp.getXML(url)
                xmlobject = xp.CaseViewer(xmlobject)
            else:
                xmlobject = XMLData[caseid]
            url_paths = _get_image_paths(xmlobject)
            case_img[caseid] = url_paths
        self.img_url_path = case_img
        if return_:
            return case_img
    
    
    def request_images(self, progress_bar=True, save_results=True, results_file='CrashViewerResults.txt'):
        '''
        Request Images
        '''
        for caseid in self.CaseID:
            MainURL = self.URL[caseid]
            case_images = self.get_img_url(return_=True, progress_bar=False) # returns dictionary
            
            data = []
            cols = ['CaseID', 'VehicleNumber', 'Category', 'Description', 'ext', 'img_url']
            for CaseID, _images in case_images.items():
                _images = list(_images)
                data.extend(_images)

            df = pd.DataFrame(data, columns = cols)
            df['VehicleNumber'] = df['VehicleNumber'].map(lambda x: x.split('-')[-1])

            download_images(MainURL=MainURL, img_info_df=df, directory=self.directory, results_file=results_file)






def download_images(MainURL, img_info_df, directory, results_file='CrashViewerResults.txt'):
    ## save file paths and data for future use
    with requests.Session() as sesh:
        for _, data in img_info_df.iterrows():
            caseid, vehicle, category, desc, ext, img_url = data
            CaseViewerPath = MainURL
            #print("Main Path", CaseViewerPath)
            #print("Current URL", img_url)
            source = sesh.get(CaseViewerPath) ## cache the session
            del source ## delete this as unneccesary
            ## first make directory
            path = os.path.join(directory, str(caseid))
            if not os.path.exists(path):
                os.makedirs(path)
            
            ## create image name
            image_name = '_'.join([caseid, vehicle, category, desc, ext])
            image_name = image_name.replace('/', '-')
            image_path = os.path.join(path, image_name)
            pull_image = sesh.get(img_url, stream=True)
            
            with open(image_path, "wb+") as myfile:
                myfile.write(pull_image.content)
                
            if results_file:
                ## save file paths and data for future use
                results_path = os.path.join(directory, caseid, results_file)
                with open(results_path, 'a+') as outfile:
                    line = '|'.join(['CaseID', 'VehicleNumber', 'Category', 'Description', 'ext', 'img_url', 'image_path'])
                    outfile.write(line + '\n')
                    line = '|'.join([caseid, vehicle, category, desc, ext, img_url, image_path])
                    outfile.write(line + '\n')





def _get_image_paths(xmlobject):
    '''
    Takes in an XML object and converts it to pynass.xmlparser.CaseViewer
    then it searches for image urls
    '''
    url_path = 'https://crashviewer.nhtsa.dot.gov/nass-cds/GetBinary.aspx?Image&ImageID={}&CaseID={}&Version={}'
    if not isinstance(xmlobject, xp.CaseViewer):
        CaseViewer = xp.CaseViewer(xmlobject)
    else:
        CaseViewer = xmlobject
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

        
