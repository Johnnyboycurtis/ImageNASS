
import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents/Model 1')
from scipy.ndimage import imread
import numpy as np
import pandas as pd
from tqdm import tqdm


traindf = pd.read_csv('traindf.csv')
n_train = traindf.shape[0]

def scale(img):
    mu = img.mean()
    sd = img.std() + 0.00001
    scaled = ((img - mu) / sd).astype('float32')
    return scaled


print("Reading in images")
pic1 = np.zeros(shape=(n_train, 600, 800, 3)) #.astype('int32')
pic2 = np.zeros(shape=(n_train, 600, 800, 3)) #.astype('int32')
Rows = traindf.iterrows()
for i, row in tqdm(Rows):
    ## pic1
    img_path = row['BackLeft']
    img = imread(img_path)
    pic1[i,:,:,:] = (img / 255).astype('float32')
    #pic1[i,:,:,:] = scale(img/255)
    ## pic2
    img_path = row['BackRight']
    img = imread(img_path)
    pic2[i,:,:,:] = (img / 255).astype('float32')
    #pic2[i,:,:,:] = scale(img / 255)




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

Adam = keras.optimizers.Adam(lr=0.0005, beta_1=0.95, beta_2=0.999, epsilon=0.00001, decay=0.00001, amsgrad=False)


print('building regression model')
# First, define the vision modules
digit_input = Input(shape=(600, 800, 3))
x = Conv2D(32, kernel_size=(3, 3), strides=(2,2))(digit_input)
x = Activation('relu')(x)
x = Conv2D(16, kernel_size=(3, 3), strides=(2,2))(x) ## change back to 16
x = Activation('relu')(x)
x = MaxPooling2D((2, 2))(x)
x = Flatten()(x)
x = Dense(32, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(16, activation='relu', kernel_initializer='random_uniform')(x)
x = Dropout(0.25)(x)
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
regression_model.compile(loss='mean_squared_error', optimizer=Adam)



print('fitting model')
regression_model.fit(x=[pic1, pic2], y = Y_train, batch_size=32, epochs=50, verbose=1, validation_split=0.20)
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
