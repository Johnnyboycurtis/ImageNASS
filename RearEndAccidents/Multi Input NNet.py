import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from sklearn.preprocessing import scale
#from tqdm import tqdm


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


np.random.seed(546)
ind = np.random.rand(4477) < 0.16
n = ind.sum()

traindf = df.loc[ind].reset_index(drop=False)

print("Reading in images")
pic1 = np.zeros(shape=(n, 600, 800, 3)).astype('int32')
pic2 = np.zeros(shape=(n, 600, 800, 3)).astype('int32')
pic3 = np.zeros(shape=(n, 600, 800, 3)).astype('int32')
for i, row in traindf.iterrows():
    ## pic1
    img_path = row['Pic1']
    img = imread(img_path)
    pic1[i,:,:,:] = img.astype('int32')
    ## pic2
    img_path = row['Pic2']
    img = imread(img_path)
    pic2[i,:,:,:] = img.astype('int32')
    ## pic3
    img_path = row['Pic3']
    img = imread(img_path)
    pic3[i,:,:,:] = img.astype('int32')



cols = 'AVG_C1 + AVG_C2 + AVG_C3 + AVG_C4 + AVG_C5 + AVG_C6 + AVG_CMAX'.split(' + ')

Y_train = traindf.loc[:, cols]
for c in cols:
    Y_train[c] = pd.to_numeric(Y_train[c], errors='coerce').fillna(0)

# dimensions of our images.
img_width, img_height = 600, 800




import keras
from keras.layers import Conv2D, MaxPooling2D, Input, Dense, Flatten, Dropout
from keras.models import Model

print('building regression model')
# First, define the vision modules
digit_input = Input(shape=(600, 800, 3))
x = Conv2D(32, (3, 3))(digit_input)
x = Conv2D(32, (3, 3))(x)
x = MaxPooling2D((2, 2))(x)
x = Flatten()(x)
x = Dense(32, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(16, activation='tanh')(x)
x = Dropout(0.5)(x)
out = Dense(7, activation='linear')(x)

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
concatenated = keras.layers.concatenate([out_a, out_b, out_c])
out = Dense(7, activation='linear')(concatenated)

regression_model = Model([digit_a, digit_b, digit_c], out)
regression_model.compile(loss='mean_squared_error', optimizer='adam')


print('fitting model')
regression_model.fit(x=[pic1, pic2, pic3], y = Y_train, batch_size=46, epochs=30, verbose=1)
## model1.json used 12% of pictures and 40 batch size

print('saving model')
# serialize model to JSON
model_json = regression_model.to_json()
with open("model2.json", "w+") as json_file:
    json_file.write(model_json)

