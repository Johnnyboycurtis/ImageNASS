"""
Created on Wed Jan 17 13:59:55 2018

@author: Jonathan Navarrete
"""
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import argparse

#usage = "ImagesRequests.py -f NASS_Sample.csv -c 8 -s , -d ~/Pictures "

parser = argparse.ArgumentParser(description='Pull images from NASS database')

parser.add_argument('Filename', metavar = 'f',
                    help='Filename of containing CaseIDs; assumes file has header')

parser.add_argument('--Column', metavar='-c', type = int, default = 8,
                    help='Column number containing Case IDs; zero based')

parser.add_argument('--Seperator', metavar='-s', default = ',',
                    help='Column seperator; default is comma')

parser.add_argument('--Destination', metavar='-d', default = '.',
                    help='Destination for files to be written')




def read_reference(filename, sep = ",", i = 8):
    with open(filename, "r") as myfile:
        print("reading Case IDs")
        header = myfile.readline()
        CaseIDs = []
        for line in myfile:
            caseid = line.strip().split(sep)[i]
            CaseIDs.append(int(caseid))
    return CaseIDs



url_part1 = 'https://www-nass.nhtsa.dot.gov/nass/cds/'


def build_urls_and_pull_images(CaseIDs):
    data = []
    with requests.Session() as sesh:
        for caseid in tqdm(CaseIDs):
            dir_name = f"CaseID_{caseid}/"
            os.mkdir(dir_name)
            url_full = f"https://www-nass.nhtsa.dot.gov/nass/cds/CaseForm.aspx?ViewText&CaseID={caseid}&xsl=textonly.xsl&websrc=true"
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
                


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    print(f"writing files in {args.Destination}")
    
    CaseIDs = read_reference(filename = args.Filename, sep = args.Seperator, i = args.Column)

    os.chdir(args.Destination)
    build_urls_and_pull_images(CaseIDs = CaseIDs)

