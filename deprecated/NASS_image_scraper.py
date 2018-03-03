"""
Created on Wed Jan 17 13:59:55 2018

@author: Jonathan Navarrete
"""
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


#CaseIDs = [149006673, 149006651, 149006672, 149006692, 149006693] ## for testing

print(f"writing files in {os.getcwd()}")


with open("CaseID_sample.csv", "r") as myfile:
    print("reading Case IDs")
    header = myfile.readline()
    CaseIDs = []
    for line in myfile:
        caseid = line.strip().split(",")[8]
        CaseIDs.append(int(caseid))



url_part1 = 'https://www-nass.nhtsa.dot.gov/nass/cds/'

data = []
with requests.Session() as sesh:
    for caseid in tqdm(CaseIDs):
        dir_name = f"CaseID_{caseid}/"
        os.mkdir(dir_name)
        url_full = f"https://www-nass.nhtsa.dot.gov/nass/cds/CaseForm.aspx?ViewText&CaseID={caseid}&xsl=textonly.xsl&websrc=true"
        #print(url_full)
        source = sesh.get(url_full).text
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
            


"""
for caseid in CaseIDs:
    url_full = f"https://www-nass.nhtsa.dot.gov/nass/cds/CaseForm.aspx?ViewText&CaseID={caseid}&xsl=textonly.xsl&websrc=true"
    print(url_full)
    source = requests.get(url_full).text
    soup = BeautifulSoup(source, 'lxml')
    
    pics = soup.find_all('tr',  style="page-break-after: always")
    break

"""
        
