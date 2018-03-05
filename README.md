# ImageNASS

> NHTSA is authorized by congress (Volume 489, United States Code Chapter 301 Motor Vehicle Safety, Section 30166, 30168 and Volume 23 , Section 403) to collect information on motor vehicle crashes to aid in the development, implementation and evaluation of motor vehicle and highway safety countermeasures. The law requires the Agency to protect the privacy of individuals involved in crashes investigated. Agency procedure for release, accuracy and security of research data collected under the NASS program prohibit the dissemination of any information collected, assembled, derived or computed until all conditions of data gathering and reporting, case completeness, quality control and privacy have been completed. The cases available through the NASS web query system have met these conditions.


The following are intended as simple scripts to extract files for anyone needing to utilize the NASS CIREN data sets and images for research.

## SAS Files

To download and extract SAS files, run

    bash ExtractNASSFiles.sh

## XML Files

To work with XML data provided by NASS, `xmlparser` provides some useful scripts to pull XML files and parse them

    import pynass.xmlparser as xp

    xmlobject = xp.Example() ## requests an XML file

    case = xp.CaseViewer(xmlobject) 
    cars = case.get_vehicles() ## get summary vehicle info

    d = xp.xml2dict(cars) ## convert XML to Python dictionary
    print(d)

## Images

On a terminal, you can run 
    
    python get_nass_images.py -h

Or, in a script
    
    import pynass.imagerequests as ir

    requester = ir.NASSImageRequest(CaseID='824229459', directory='./Pictures')
    requester.URL ## to see URLs
    requester.pull_images()


## Case Search

To find case numbers, SearchNASS class allows you to specify search parameters available in Case Viewer.

    import pynass.casesearch as cs

    casefinder = cs.SearchNASS('../../chromedriver')
    results = casefinder.Search(PlaneOfImpact='Front', Year='2015', Month='Jun')
    print(results)



