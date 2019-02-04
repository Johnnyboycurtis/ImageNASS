# ImageNASS

The following project intends to provide simple to use API and scripts to extract files for anyone needing to utilize the [NASS CDS Crash Viewer](https://crashviewer.nhtsa.dot.gov/LegacyCDS/Search) data sets and images for research.

## About Crashworthiness Data System (CDS)

> The Crash Investigation Sampling System (CISS) has detailed data on a nationally representative sample of thousands of passenger vehicle crashes. Trained Crash Technicians collect information from crash sites, vehicles, victims, and medical records. CISS data is used by government, industry, academia, and other stakeholders to analyze crashes and injuries.

> The Crashworthiness Data System (CDS) was the precursor to CISS.

> NHTSA is authorized by congress (Volume 489, United States Code Chapter 301 Motor Vehicle Safety, Section 30166, 30168 and Volume 23 , Section 403) to collect information on motor vehicle crashes to aid in the development, implementation and evaluation of motor vehicle and highway safety countermeasures. The law requires the Agency to protect the privacy of individuals involved in crashes investigated. Agency procedure for release, accuracy and security of research data collected under the NASS program prohibit the dissemination of any information collected, assembled, derived or computed until all conditions of data gathering and reporting, case completeness, quality control and privacy have been completed. The cases available through the NASS web query system have met these conditions.




## SAS Files

To download and extract SAS files, run

    bash ExtractNASSFiles.sh

## XML Files

To work with XML data provided by NASS, `xmlparser` provides some useful scripts to pull XML files and parse them

    import pynass.xmlparser as xp

    xmlobject = xp._Example() ## requests an XML file

    case = xp.CaseViewer(xmlobject) 
    cars = case.get_vehicles() ## get summary vehicle info

    d = xp.xml2dict(cars) ## convert XML to Python dictionary
    print(d)

    {'NumberVehicles': '2',
    'VehicleSum1': {'Year': '1998',
    'Make': 'DODGE',
    'Model': 'STRATUS',
    'DamagePlane': 'Front',
    'Severity': 'Moderate',
    'ComponentFailure': 'none'},
    'VehicleSum2': {'Year': '1997',
    'Make': 'CHRYSLER',
    'Model': 'LHS',
    'DamagePlane': 'Left',
    'Severity': 'Moderate',
    'ComponentFailure': 'none'}}

## Images

On a system terminal, you can run 
    
    python get_nass_images.py -h

Or, in a Python script

    import pynass.imagerequests as ir

    CaseIDList = ['208017535', '141017241', '208017555', '208018415'] # NASS case ID list

    # construct requesting object
    requester = ir.CrashViewerImageRequest(CaseID = CaseIDList, directory='./Pictures', XMLData=None)
    # obtain all case URL sites
    requester.CrashViewerURL()
    # download images
    requester.request_images()



## Case Search

## API

To find case numbers, SearchNASS class allows you to specify search parameters available in Case Viewer.

    import pynass.casesearch as cs

    casefinder = cs.SearchNASS('../../chromedriver')
    results = casefinder.Search(PlaneOfImpact='Front', Year='2015', Month='Jun')
    print(results)


### ChromeDriver

The `pynass.casesearch` module utilizes chromedriver. Other drivers are available to use, however, those were not implemented in this project. A custom script will be needed to utilze another driver. You can find the [ChromeDriver](http://chromedriver.chromium.org) provided by the Chromium Project.
