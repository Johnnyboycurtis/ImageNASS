import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(546789)


def update_names(imgpath):
    pictures = '/home/jn107154/Pictures'
    img_name = imgpath.split('/')[-1]
    caseid = imgpath.split('/')[-2]
    new_path = os.path.join(pictures, caseid, 'resized', img_name)
    return new_path


InputDF = pd.read_csv('InputDF.csv', dtype={'CaseID':str})  ## has old paths

back_end_ = pd.read_csv("Back_End.csv", dtype={'CaseID':str, 'VehicleNumber':str}, na_values='Unknown')
back_end_.head()

rear_events = pd.read_csv('rear_events.csv', dtype={'CaseID':str, 'VehicleNumber':str, 'ContactedVehicleNumber':str}, na_values='Unknown')
rear_events.head()

back_end_events = pd.merge(left = back_end_, right = rear_events, on = ['CaseID', 'VehicleNumber'])


df = pd.merge(left=back_end_events, right = InputDF, on = 'CaseID')
df = df.sample(frac=1).reset_index(drop=True)


df['Pic1'] = df['Pic1'].map(update_names)
df['Pic2'] = df['Pic2'].map(update_names)
df['Pic3'] = df['Pic3'].map(update_names)

def search_child_seat(imgname):
    imgname = imgname.upper()
    if 'CHILD' in imgname or 'RESTRAINT' in imgname:
        return True
    else:
        return False

nochild = ~df.apply(lambda row: search_child_seat(row['Pic1']) or search_child_seat(row['Pic2']) or search_child_seat(row['Pic3']), axis=1)

ind = ~df.Total.isnull().values
df = df.loc[ind & nochild]
n = df.shape[0]



ind = np.random.rand(n) < 0.2


traindf = df.loc[ind].reset_index(drop=False)
n_train = traindf.shape[0]

print("Reading in images")
pic1 = np.zeros(shape=(n_train, 600, 800, 3)).astype('int32')
pic2 = np.zeros(shape=(n_train, 600, 800, 3)).astype('int32')
pic3 = np.zeros(shape=(n_train, 600, 800, 3)).astype('int32')
for i, row in traindf.iterrows():
    ## pic1
    img_path = row['Pic1']
    img = imread(img_path)
    pic1[i,:,:,:] = img / 255
    ## pic2
    img_path = row['Pic2']
    img = imread(img_path)
    pic2[i,:,:,:] = img / 255
    ## pic3
    img_path = row['Pic3']
    img = imread(img_path)
    pic3[i,:,:,:] = img / 255





from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K



cols = 'AVG_C1 + AVG_C2 + AVG_C3 + AVG_C4 + AVG_C5 + AVG_C6'.split(' + ')

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
model.add(Dense(6))
model.add(Activation('linear'))

model.compile(loss='mean_squared_error', optimizer='adam')

model.fit(pic1, Y_train, batch_size=32, epochs=3, verbose=1)



print('predictions')
pred = model.predict(pic1[20:24,:,:,:], verbose=1)
print(pred)




