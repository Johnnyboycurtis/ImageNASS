"""
Requests images from NASS Crash Viewer
"""

import os
import xmlparser as xp
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from joblib import Parallel, delayed



class NASSImageRequest():
    
    def __init__(self, CaseID, directory):
        """
        Builds URLs to images in NASS database and downloads images to specified directory
        """
        self.CaseID = CaseID
        self.directory = directory
        self.URL = self.generate_URL()
    
    def generate_URL(self):
        "Generate URLs for NASS image scraper"
        URL = dict()
        for caseid in self.CaseID:
            url_full = "https://crashviewer.nhtsa.dot.gov/nass-cds/CaseForm.aspx?ViewText&CaseID={}&xsl=textonly.xsl&websrc=true".format(caseid)
            URL[caseid] = url_full
        return URL

    def pull_images(self, progress_bar=True):
        url_part1 = 'https://crashviewer.nhtsa.dot.gov/nass-cds/'
        dir_name = self.directory
        URL = self.URL.items()
        if progress_bar:
            URL = tqdm(self.URL.items())
        with requests.Session() as sesh:
            for caseid, line in URL:
                ## first make directory
                path = os.path.join(dir_name, str(caseid))
                if not os.path.exists(path):
                    os.makedirs(path)
                ## next, get HTML data
                source = sesh.get(line).text
                soup = BeautifulSoup(source, 'lxml')
                tr_tags = soup.find_all('tr',  style="page-break-after: always")
                if progress_bar:
                    tr_tags = tqdm(tr_tags)
                for tag in tr_tags:
                    tag_list = tag.find_all('tr', class_ = 'label') ## get all tag labels
                    ## get image_id, image type, and part name
                    img_id, img_type, part_name = [x.find('td').text for x in tag_list] 
                    img_type = img_type.replace(" - image", "")
                    img_id = img_id.replace(":", "")
                    part_name = part_name.replace(":", "").replace("/", "")
                    image_name = "_".join([img_type, part_name, img_id]) + ".jpg"
                    image_name = os.path.join(path, image_name)
                    ## next, build the img url
                    img = tag.find('img')
                    url_src = img.get('src')
                    img_url =  url_part1 + url_src
                    #print('IMAGE URL', img_url)
                    #print('Saving to: ', image_name)
                    pull_image = sesh.get(img_url, stream=True)
                    with open(image_name, "wb+") as myfile:
                        myfile.write(pull_image.content)





class CrashViewerImageRequest():
    def __init__(self, CaseID, directory):
        """
        Builds URLs to images in NHTSA Crash Viewer
        """
        self.CaseID = CaseID ## iterable
        self.directory = directory
        self.URL = self.CrashViewerURL() ## URL to Case Viewer
    
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
            
    
    def get_img_url(self, store=False, return_=False, progress_bar=True):
        '''
        Extract image URLs from XML data. 
        If `store = True`, saves XML data to self.XMLData
        If `return_ = True`, returns dict of image URL paths
        '''
        URL = self.URL
        XMLData = dict()
        case_img = dict()
        URL_items = URL.items()
        if progress_bar:
            URL_items = tqdm(URL_items)
        for caseid, url in URL_items:
            xmlobject = xp.getXML(url)
            if store:
                XMLData[caseid] = xmlobject
            url_paths = _get_image_paths(xmlobject)
            case_img[caseid] = url_paths
        self.img_url_path = case_img
        if store:
            self.XMLData = XMLData
        if return_:
            return case_img
    
    
    def request_images(self, progress_bar=True, save_results=True, results_file='CrashViewerResults.txt'):
        '''
        Request Images
        '''
        directory = self.directory
        
        if save_results:
            ## save file paths and data for future use
            results_path = os.path.join(directory, results_file)
            with open(results_path, 'a+') as outfile:
                line = '|'.join(['CaseID', 'VehicleNumber', 'Category', 'Description', 'ext', 'img_url', 'image_path'])
                outfile.write(line + '\n')
        
        img_url_path = self.img_url_path.values()
        img_url_path = flattenList(list(img_url_path))
        
        if progress_bar:
            img_url_path = tqdm(img_url_path)
            
        with requests.Session() as sesh:
            for caseid, vehicle, category, desc, ext, img_url in img_url_path:
                CaseViewerPath = self.URL[caseid]
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
                    
                if save_results:
                    ## save file paths and data for future use
                    results_path = os.path.join(directory, results_file)
                    with open(results_path, 'a+') as outfile:
                        line = '|'.join([caseid, vehicle, category, desc, ext, img_url, image_path])
                        outfile.write(line + '\n')


    def parallel_images(self, progress_bar=True, save_results=True, results_file='CrashViewerResults.txt'):
        '''
        PARALLEL Request Images
        '''
        directory = self.directory
        
        
        if save_results:
            ## save file paths and data for future use
            results_path = os.path.join(directory, results_file)
            with open(results_path, 'a+') as outfile:
                line = '|'.join(['CaseID', 'VehicleNumber', 'Category', 'Description', 'ext', 'img_url', 'image_path'])
                outfile.write(line + '\n')
        
        img_url_path = self.img_url_path.values()
        img_url_path = flattenList(list(img_url_path))
        img_url_path = [list(args) for args in img_url_path]
        
        Args = []
        
        URLDict = self.URL
        for line in img_url_path:
            line.append(directory)
            line.append(URLDict)
            line.append(results_file)
            Args.append(line)
        
        Parallel(n_jobs=4)(delayed(multi_run_wrapper)(args) for args in Args)
                



def multi_run_wrapper(args):
       return _myfun(*args)
            
def _myfun(caseid, vehicle, category, desc, ext, img_url, directory, URLDict, results_file=None):
    with requests.Session() as sesh:
        CaseViewerPath = URLDict[caseid] ## url dict
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

        
            
            


#https://crashviewer.nhtsa.dot.gov/nass-cds/GetBinary.aspx?Image&ImageID=498459125&CaseID=211017160&Version=1
#https://crashviewer.nhtsa.dot.gov/nass-cds/GetBinary.aspx?Image&ImageID=498459091&CaseID=211017160&Version=0
#https://crashviewer.nhtsa.dot.gov/nass-cds/GetBinary.aspx?Image&ImageID=211485731&CaseID=211017982&Version=1
