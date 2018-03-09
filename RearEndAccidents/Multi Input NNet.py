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



ind = np.random.rand(n) < 0.50


traindf = df.loc[ind].reset_index(drop=False)
n_train = traindf.shape[0]

print("Reading in images")
pic1 = np.zeros(shape=(n_train, 600, 800, 3)) #.astype('int32')
pic2 = np.zeros(shape=(n_train, 600, 800, 3)) #.astype('int32')
pic3 = np.zeros(shape=(n_train, 600, 800, 3)) #.astype('int32')
for i, row in traindf.iterrows():
    ## pic1
    img_path = row['Pic1']
    img = imread(img_path)
    pic1[i,:,:,:] = (img / 255).astype('float32')
    ## pic2
    img_path = row['Pic2']
    img = imread(img_path)
    pic2[i,:,:,:] = (img / 255).astype('float32')
    ## pic3
    img_path = row['Pic3']
    img = imread(img_path)
    pic3[i,:,:,:] = (img / 255).astype('float32')




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
digit_c = Input(shape=(600, 800, 3))

# The vision model will be shared, weights and all
out_a = vision_model(digit_a)
out_b = vision_model(digit_b)
out_c = vision_model(digit_c)

# Then concat all three input models
concatenated = keras.layers.average([out_a, out_b, out_c])
out = Dense(m, activation='linear')(concatenated)

regression_model = Model([digit_a, digit_b, digit_c], out)
regression_model.compile(loss='mean_squared_error', optimizer='adam')



print('fitting model')
regression_model.fit(x=[pic1, pic2, pic3], y = Y_train, batch_size=32, epochs=25, verbose=1, validation_split=0.20)
## model1.json used 12% of pictures and 40 batch size


print('predictions')
pred = regression_model.predict([pic1[10:24,:,:,:], pic2[10:24,:,:,:], pic3[10:24,:,:,:]], verbose=1)
print(pred)

print('actual values')
print(Y_train.iloc[10:24, :])


print('saving model')
# serialize model to JSON
model_json = regression_model.to_json()
with open("model.json", "w+") as json_file:
    json_file.write(model_json)
    
# serialize weights to HDF5
regression_model.save_weights("model.h5")
print("Saved model to disk")


