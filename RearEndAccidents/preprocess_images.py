import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm


InputDF = pd.read_csv('InputDF.csv', dtype=str)



tmp = imread(fname = '/home/jn107154/Pictures/126013662/resized/Vehicle 2_back_Image ID 687161496.jpg')
plt.imshow(tmp)


#resizetest = imresize(tmp, size=(600, 800, 3))
#plt.imshow(resizetest)


jpgfiles = []
for i, row in InputDF[['Pic1', 'Pic2', 'Pic3']].iterrows():
    jpgfiles += row.tolist()
jpgfiles = list(set(jpgfiles))



pictures = '/home/jn107154/Pictures'
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
    
    
    
def update_names(imgpath):
    pictures = '/home/jn107154/Pictures'
    img_name = imgpath.split('/')[-1]
    caseid = imgpath.split('/')[-2]
    new_path = os.path.join(pictures, caseid, 'resized', img_name)
    return new_path
    
    
    
#InputDF['Pic1'].head().map(update_names)
    

back_end_ = pd.read_csv("Back_End.csv", dtype=str)
back_end_.head()

df = pd.merge(left=back_end_, right = InputDF, on = 'CaseID')
df['Pic1'] = df['Pic1'].map(update_names)
df['Pic2'] = df['Pic2'].map(update_names)
df['Pic3'] = df['Pic3'].map(update_names)


pic1 = np.zeros(shape=(4477, 600, 800, 3))
for i, row in df.iterrows():
    img_path = row['Pic1']
    img = imread(img_path)
    pic1[i,:,:,:] = img

