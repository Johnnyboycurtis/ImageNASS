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




#https://crashviewer.nhtsa.dot.gov/nass-cds/GetBinary.aspx?Image&ImageID=498459125&CaseID=211017160&Version=1
#https://crashviewer.nhtsa.dot.gov/nass-cds/GetBinary.aspx?Image&ImageID=498459091&CaseID=211017160&Version=0
#https://crashviewer.nhtsa.dot.gov/nass-cds/GetBinary.aspx?Image&ImageID=211485731&CaseID=211017982&Version=1
