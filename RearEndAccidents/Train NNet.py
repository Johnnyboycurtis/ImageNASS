import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
import patsy


def update_names(imgpath):
    pictures = '/home/jn107154/Pictures'
    img_name = imgpath.split('/')[-1]
    caseid = imgpath.split('/')[-2]
    new_path = os.path.join(pictures, caseid, 'resized', img_name)
    return new_path


InputDF = pd.read_csv('InputDF.csv', dtype={'CaseID':str})  ## has old paths

back_end_ = pd.read_csv("Back_End.csv", dtype={'CaseID':str})
back_end_.head()

df = pd.merge(left=back_end_, right = InputDF, on = 'CaseID')
df['Pic1'] = df['Pic1'].map(update_names)
df['Pic2'] = df['Pic2'].map(update_names)
df['Pic3'] = df['Pic3'].map(update_names)


ind = np.random.rand(4477) < 0.2
n = ind.sum()

traindf = df.loc[ind].reset_index(drop=False)

pic1 = np.zeros(shape=(n, 600, 800, 3))
pic2 = np.zeros(shape=(n, 600, 800, 3))
pic3 = np.zeros(shape=(n, 600, 800, 3))
for i, row in traindf.iterrows():
    ## pic1
    img_path = row['Pic1']
    img = imread(img_path).astype('float32')
    pic1[i,:,:,:] = img
    ## pic2
    img_path = row['Pic2']
    img = imread(img_path).astype('float32')
    pic2[i,:,:,:] = img
    ## pic3
    img_path = row['Pic3']
    img = imread(img_path).astype('float32')
    pic3[i,:,:,:] = img





from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K



cols = 'AVG_C1 + AVG_C2 + AVG_C3 + AVG_C4 + AVG_C5 + AVG_C6 + AVG_CMAX'.split(' + ')

Y_train = traindf.loc[:, cols]
for c in cols:
    Y_train[c] = pd.to_numeric(Y_train[c], errors='coerce').fillna(0)

# dimensions of our images.
img_width, img_height = 600, 800


model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(600,800,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(7))
model.add(Activation('linear'))

model.compile(loss='mean_squared_error', optimizer='adam')

model.fit(pic1, Y_train, batch_size=32, epochs=20, verbose=1)




stuff = model.predict(x = pic1)




