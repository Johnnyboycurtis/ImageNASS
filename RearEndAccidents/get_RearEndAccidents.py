

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
        _summary[car] = Contacted
    events[caseid] = _summary



"""
## find delta v values ##
"""
a,b = tmp.GeneralVehicleForms.findall('GeneralVehicleForm')
## <GeneralVehicleForm CaseID="923019344" VehicleNumber="1" VehicleID="923675865" CDStype="1">
list(a.items()) ## basically, a dictionary
#Out[47]: 
#[('CaseID', '209018740'),
# ('VehicleNumber', '1'),
# ('VehicleID', '209504317'),
# ('CDStype', '1')]


deltav = list()
for caseid, tmp in cases.items():
    GenVehicleForm = tmp.GeneralVehicleForms
    ## for each Case, look at the General Vehicle Forms for each car
    for tmpdata in GenVehicleForm:
        VehicleNumber = tmpdata.get('VehicleNumber')
        DV = tmpdata.find('DeltaV')
        Event = DV.find('Event')
        ComputedDV = Event.find('ComputerGeneratedDeltaV') ## get delta v data
        vehicledv = xp.xml2dict(ComputedDV)
        vehicledv['VehicleNumber'] = VehicleNumber
        dvUOM = ComputedDV.find('Total').get('UOM')
        vehicledv['DeltaVUOM'] =  dvUOM
        BarrierEquivalentSpeed = Event.find('BarrierEquivalentSpeed')
        barrier = xp.xml2dict(BarrierEquivalentSpeed)
        barrierUOM = BarrierEquivalentSpeed.get('UOM')
        vehicledv['BarrierEquivalentSpeed'] = barrier
        vehicledv['BarrierUOM'] = barrierUOM
        vehicledv['CaseID'] = caseid
        deltav.append(vehicledv)

deltavdf = pd.DataFrame(deltav)
print(deltavdf.head())













