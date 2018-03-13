
import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents/Model 1')
import pandas as pd
import numpy as np


vehicle_struck = pd.read_csv('../Vehicle Struck.csv', index_col = 0)

vehicle_struck_dict = vehicle_struck.to_dict()['VehicleNumber']

## locate images

from glob import glob

def check_back_bumber(imgname):
    imgname = imgname.upper()
    words = ['BACK'] ## back, rear, bumper
    for w in words:
        check = w in imgname
        if check:
            break
    not_needed = ['TIRE', 'COVER', 'SEAT', 'CHILD', 'RESTRAINT', 'INTERIOR', 'BASE', 'FRONT']
    for tag in not_needed:
        if tag in imgname:
            check = False
    return check


def is_back_img(imgname):
    imgname = imgname.upper()
    check = check_back_bumber(imgname)
    if check:
        if 'LEFT' in imgname:
            return 'BACKLEFT'
        elif 'RIGHT' in imgname:
            return 'BACKRIGHT'
    else:
        return None
    


filenames = dict()

for caseid, car in vehicle_struck_dict.items():
    vehicle_num = 'Vehicle-{}'.format(car)
    files = glob('/home/jn107154/Pictures/NASS/{}/*{}*.jpg'.format(caseid, vehicle_num))
    data = []
    for imgname in files:
        back_img = is_back_img(imgname)
        if caseid == '491015034':
            print(imgname, check)
        if back_img:
            data.append((back_img, imgname))
    filenames[caseid] = data


counts = []
for caseid, images in filenames.items():
    counts.append((caseid, len(images)))

counts.sort(key=lambda x: x[1])



"""
Create a data reference
"""
import itertools as it

InputData = list()
for caseid, tmp in filenames.items():        
    back_left_iter = filter(lambda x: x[0] == 'BACKLEFT', tmp)
    back_left_images = [img for _, img in back_left_iter]
    back_right_iter = filter(lambda x: x[0] == 'BACKRIGHT', tmp)
    back_right_images = [img for _, img in back_right_iter]
    Combos = it.product(back_left_images, back_right_images)
    for combo in Combos:
        if len(combo) > 0:
            combo = list(combo)
            combo.append(caseid)
            InputData.append(combo)


InputDF = pd.DataFrame(InputData, columns=['BackLeft', 'BackRight', 'CaseID'])
print(InputDF.head(10))
InputDF.to_csv('InputDF.csv', index=False)



InputDF = pd.read_csv('InputDF.csv')







"""
DATA FIXES BELOW
"""


## there are some caseids without images
## there are also some errors in caseviewer
## Compare summary vs events
# https://crashviewer.nhtsa.dot.gov/nass-cds/CaseForm.aspx?xsl=main.xsl&CaseID=900015926


zeros = []
for caseid, images in filenames.items():
    if len(images) == 0:
        zeros.append(caseid)
print(len(zeros))

vehicle_struck['900015926'] = '1' ## correction
vehicle_struck['126015378'] = '1' ## correction
## 498015280 ## no pictures
vehicle_struck['502017236'] = '1'
vehicle_struck['539016344'] = '1'
vehicle_struck['540017877'] = '1'
vehicle_struck['760013073'] = '1'
vehicle_struck['760013594'] = '1'
vehicle_struck['760014153'] = '1'
vehicle_struck['765012694'] = '1'
vehicle_struck['769014857'] = '1'
vehicle_struck['900015926'] = '1'
vehicle_struck['923018141'] = '1'
vehicle_struck['211017261'] = '1'
vehicle_struck['502017236'] = '2'



