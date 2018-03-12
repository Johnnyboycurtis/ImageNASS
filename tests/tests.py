#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:31:19 2018

@author: jn107154
"""

import sys
sys.path.append('../')

from pynass.imagerequests import CrashViewerImageRequest       



test = CrashViewerImageRequest(CaseID = ['114005998'], directory = '/tmp/')

test.CrashViewerURL()
print('CaseViewerURL', test.URL)

test.get_img_url()
print('image url paths', test.img_url_path.values())

test.request_images()   