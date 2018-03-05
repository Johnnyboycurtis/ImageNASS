

import os
os.chdir('/home/jn107154/Documents/ImageNASS')
import sys
sys.path.append('../')
import pynass.casesearch as cs
import pynass.xmlparser as xp
import pandas as pd
import numpy as np

## get Rear end accidents for 2014-2015
finder = cs.SearchNASS()

results = []
for year in [2010, 2011, 2012, 2013, 2014, 2015]:
    tmp = finder.Search(PlaneOfImpact='Back (Rear)', Year = year, MinVeh=2, MaxVeh=2, Make = 'HONDA')
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
cases = dict()
severity = []
for caseid in results:
    url = xp.buildURL(caseid)
    data = xp.getXML(url, verbose=True)
    tmp = xp.CaseViewer(data)
    cases[caseid] = tmp
    

severity = []
i = 0
for caseid, tmp in cases.items():
    vehicles = tmp.get_vehicles()
    vehicles = xp.xml2dict(vehicles)
    vehicles.pop('NumberVehicles')
    for car, tmpdata in vehicles.items():
        i += 1
        val = tmpdata.get('Severity', 'Unknown')
        if val is not None:
            severity.append(val)
    #break


stuff = np.unique(severity, return_counts=True)
dict(zip(*stuff))




events = dict()
for caseid, tmp in cases.items():
    _events = tmp.get_events()
    _events = xp.xml2dict(_events)
    _summary = dict()
    for i, items in enumerate(_events.items(), 1):
        car, tmpdata = items
        Contacted = tmpdata.get('Contacted', 'N/A')
        VEHICLE = 'Vehicle#{}'.format(i)
        _summary[car] = contacted
    events[caseid] = _summary







