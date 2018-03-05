

import os
os.chdir('/home/jn107154/Documents/ImageNASS')
import sys
sys.path.append('../')
import pynass.casesearch as cs
import pynass.xmlparser as xp
import pandas as pd


## get Rear end accidents for 2014-2015
finder = cs.SearchNASS()

results = []
for year in [2013, 2014, 2015]:
    tmp = finder.Search(PlaneOfImpact='Back (Rear)', Year = 2015, Month = 'All', Make = 'HONDA')
    ## tmp is a dictionary, but I only want/need the caseid not the links
    results += tmp

## save case ids
with open("RearEndCases.txt", "w+") as myfile:
    for line in results:
        myfile.write(line + '\n')


results = []
with open('RearEndCases.txt') as myfile:
    for line in myfile:
        results.append(line.strip())

## get xml data
for caseid in results:
    url = xp.buildURL(caseid)
    data = xp.getXML(url)
    tmp = xp.CaseViewer(data)
    vehicles = tmp.get_vehicles()
    vehicles = xp.xml2dict(vehicles)
    vehicles.pop('NumberVehicles')
    df = pd.DataFrame(vehicles)
    break
    




