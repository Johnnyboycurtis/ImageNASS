"""
Requests images from NASS Crash Viewer
"""

import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class NASSImageRequest():
    def __init__(self, CaseID, directory):
        """
        Builds URLs to images in NASS database and downloads images to specified directory
        """
        if isinstance(CaseID, list) or isinstance(CaseIDs, tuple):
            CaseID = [CaseID]
        self.CaseID = CaseID
        self.directory = directory
        self.URL = self.generate_URL()
    
    def generate_URL():
        "Generate URLs for NASS image scraper"
        URL = []
        for caseid in self.CaseID:
            url_full = "https://crashviewer.nhtsa.dot.gov/nass-sci/CaseForm.aspx?ViewText&CaseID={}&xsl=textonly.xsl&websrc=true".format(caseid)
            URL.append(url_full)
        return URL

    def pull_images(progress_bar=True):
        URL = self.URL
        if progress_bar:
            URL = tqdm(self.URL)
        with requests.Session() as sesh:
            for line in URL:
                source = sesh.get(line).text
                soup = BeautifulSoup(source, 'lxml')
                tr_tags = soup.find_all('tr',  style="page-break-after: always")
                for tag in tr_tags:
                    tag_list = tag.find_all('tr', class_ = 'label') ## get all tag labels
                    ## get image_id, image type, and part name
                    img_id, img_type, part_name = [x.find('td').text for x in tag_list] 
                    img_type = img_type.replace(" - image", "")
                    img_id = img_id.replace(":", "")
                    part_name = part_name.replace(":", "").replace("/", "")
                    image_name = dir_name + "_".join([img_type, part_name, img_id]) + ".jpg"
                    ## next, build the img url
                    img = tag.find('img')
                    url_src = img.get('src')
                    img_url =  url_part1 + url_src
                    #print(img_url)
                    pull_image = sesh.get(img_url, stream=True)
                    with open(image_name, "wb+") as myfile:
                        myfile.write(pull_image.content)
