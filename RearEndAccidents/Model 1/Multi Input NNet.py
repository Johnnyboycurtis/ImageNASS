import sys
import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents/Model 1')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

np.random.seed(123546789)


def update_names(imgpath):
    pictures = '/home/jn107154/Pictures/NASS/'
    img_name = imgpath.split('/')[-1]
    caseid = imgpath.split('/')[-2]
    new_path = os.path.join(pictures, caseid, 'resized', img_name)
    return new_path


InputDF = pd.read_csv('InputDF.csv', dtype={'CaseID':str})  ## has images with old paths

back_end_ = pd.read_csv("../Back_End.csv", dtype={'CaseID':str, 'VehicleNumber':str}, na_values='Unknown') ## data
back_end_.head()

rear_events = pd.read_csv('../rear_events.csv', dtype={'CaseID':str, 'VehicleNumber':str, 'ContactedVehicleNumber':str}, na_values='Unknown')  ## data
rear_events.head()

back_end_events = pd.merge(left = back_end_, right = rear_events, on = ['CaseID', 'VehicleNumber'])


df = pd.merge(left=back_end_events, right = InputDF, on = 'CaseID')
df = df.sample(frac=1).reset_index(drop=True)

df['BackLeft'] = df['BackLeft'].map(update_names)
df['BackRight'] = df['BackRight'].map(update_names)

ind = ~df.Total.isnull().values
df = df.loc[ind]
n = df.shape[0]
print('Number of Records', n)



ind = np.random.rand(n) < 0.75


traindf = df.loc[ind].reset_index(drop=False)
n_train = traindf.shape[0]
print('Number of Training Records', n_train)

print("Reading in images")
pic1 = np.zeros(shape=(n_train, 600, 800, 3)) #.astype('int32')
pic2 = np.zeros(shape=(n_train, 600, 800, 3)) #.astype('int32')
Rows = traindf.iterrows()
for i, row in tqdm(Rows):
    ## pic1
    img_path = row['BackLeft']
    img = imread(img_path)
    pic1[i,:,:,:] = (img / 255).astype('float32')
    ## pic2
    img_path = row['BackRight']
    img = imread(img_path)
    pic2[i,:,:,:] = (img / 255).astype('float32')




#cols = 'AVG_C1 + AVG_C2 + AVG_C3 + AVG_C4 + AVG_C5 + AVG_C6 + BarrierEquivalentSpeed +  EnergyAbsorption + Total'.split(' + ')
cols = 'Total'.split(' + ')

m = len(cols)

Y_train = traindf.loc[:, cols]
for c in cols:
    Y_train[c] = pd.to_numeric(Y_train[c], errors='coerce').fillna(0)

# dimensions of our images.
img_width, img_height = 600, 800




import keras
from keras.layers import Conv2D, MaxPooling2D, Input, Dense, Flatten, Dropout, Activation
from keras.models import Model

print('building regression model')
# First, define the vision modules
digit_input = Input(shape=(600, 800, 3))
x = Conv2D(32, kernel_size=(6, 6), strides=(3,3))(digit_input)
x = Activation('relu')(x)
x = Conv2D(16, kernel_size=(6, 6), strides=(3,3))(x)
x = Activation('relu')(x)
x = MaxPooling2D((2, 2))(x)
x = Flatten()(x)
x = Dense(32, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(16, activation='relu', kernel_initializer='random_uniform')(x)
x = Dropout(0.15)(x)
out = Dense(m, activation='linear', kernel_initializer='random_uniform')(x)

vision_model = Model(digit_input, out)

# Then define the tell-digits-apart model
digit_a = Input(shape=(600, 800, 3))
digit_b = Input(shape=(600, 800, 3))

# The vision model will be shared, weights and all
out_a = vision_model(digit_a)
out_b = vision_model(digit_b)

# Then concat all three input models
concatenated = keras.layers.average([out_a, out_b])
out = Dense(m, activation='linear')(concatenated)

regression_model = Model([digit_a, digit_b], out)
regression_model.compile(loss='mean_squared_error', optimizer='adam')



print('fitting model')
regression_model.fit(x=[pic1, pic2], y = Y_train, batch_size=32, epochs=20, verbose=1, validation_split=0.20)
## model1.json used 12% of pictures and 40 batch size


print('predictions')
pred = regression_model.predict([pic1[10:24,:,:,:], pic2[10:24,:,:,:]], verbose=1)
print(pred)

print('actual values')
print(Y_train.iloc[10:24, :])


print('saving model')
# serialize model to JSON
model_json = regression_model.to_json()
with open("model-1.json", "w+") as json_file:
    json_file.write(model_json)
    
# serialize weights to HDF5
regression_model.save_weights("model-1.h5")
print("Saved model to disk")
