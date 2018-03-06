import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents')
import sys
sys.path.append('../')
import pynass.imagerequests as ir


with open('RearEndCases.txt', 'r') as myfile:
    CaseIDs = []
    for line in myfile:
        CaseIDs.append(line.strip())
        


requester = ir.NASSImageRequest(CaseID=CaseIDs, directory='/home/jn107154/Pictures/')
requester.URL ## to see URLs
requester.pull_images(progress_bar=True)



