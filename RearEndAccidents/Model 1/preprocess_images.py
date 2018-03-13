import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents/Model 1')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm


InputDF = pd.read_csv('InputDF.csv', dtype=str)

jpgfiles = []
for i, row in InputDF[['BackLeft', 'BackRight']].iterrows():
    jpgfiles += row.tolist()
jpgfiles = list(set(jpgfiles))



pictures = '/home/jn107154/Pictures/NASS'
for fname in tqdm(jpgfiles):
    ## build path name
    img_name = fname.split('/')[-1]
    caseid = fname.split('/')[-2]
    path = os.path.join(pictures, caseid, 'resized')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, img_name)
    ## read in image
    tmpimage = imread(fname=fname)
    shape = tmpimage.shape
    resized_img = imresize(tmpimage, size=(600, 800, 3))    ## resize image
    imsave(path,resized_img)

