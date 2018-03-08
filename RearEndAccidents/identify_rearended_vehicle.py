
import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents')
import pandas as pd
import numpy as np



crushprofiles = pd.read_csv('CrushProfiles.csv', dtype=str)

crushprofiles[['CaseID','DirectDamageLocation']].tail(10) ## /home/jn107154/Pictures/703018860
ind = crushprofiles['CaseID'] == '703018860'
crushprofiles.loc[ind]



rear_events = pd.read_csv('rear_events.csv', dtype = str)
rear_events.head()

def fix_cvn(row):
    if row.ContactedAreaOfDamage == 'Front':
        if row.VehicleNumber == '1':
            row['ContactedVehicleNumber'] = '1'
        else:
            row['ContactedVehicleNumber'] = '2'
    return row

rear_events.loc[rear_events['CaseID'] == '703018860']

groupedres = rear_events.groupby(by='CaseID')['ContactedVehicleNumber'].unique()


def drop_nan(array):
    array = np.array(array)
    ind = pd.isnull(array)
    array = array[~ind]
    if len(array) > 0:
        return array
    else:
        return [np.nan]


vehicle_struck = groupedres.apply(lambda x: drop_nan(x)[0]).dropna()

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



vehicle_struck_dict = vehicle_struck.to_dict()
vehicle_struck = vehicle_struck.to_frame('VehicleNumber')


## merge crush profiles with those vehicles that were rear ended
back_end_ = pd.merge(left = crushprofiles, right = vehicle_struck.reset_index(), on = ['CaseID', 'VehicleNumber'])

back_end_.to_csv("Back_End.csv", index=False)

vehicle_struck.to_csv('Vehicle Struck.csv', index=True)





## locate images

from glob import glob

def check_back_bumber(imgname):
    imgname = imgname.upper()
    words = ['BACK'] ## back, rear, bumper
    for w in words:
        check = w in imgname
        if check:
            break
    if 'TIRE' in imgname or 'COVER' in imgname or  'SEAT' in imgname or 'CHILD' in imgname or 'RESTRAINT' in imgname or 'BASE' in imgname:
        check = False
    return check



filenames = dict()

for caseid, car in vehicle_struck_dict.items():
    vehicle_num = 'Vehicle {}'.format(car)
    files = glob('/home/jn107154/Pictures/{}/*{}*.jpg'.format(caseid, vehicle_num))
    data = []
    for imgname in files:
        check = check_back_bumber(imgname)
        if caseid == '491015034':
            print(imgname, check)
        if check:
            data.append(imgname)
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
    tmp = it.combinations(tmp, r=3)
    for combo in tmp:
        if len(combo) > 0:
            combo = list(combo)
            combo.append(caseid)
            InputData.append(combo)


InputDF = pd.DataFrame(InputData, columns=['Pic1', 'Pic2', 'Pic3', 'CaseID'])
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



