import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents/Model 1')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

def scale(img):
    mu = img.mean()
    sd = img.std() + 0.00001
    scaled = ((img - mu) / sd).astype('float32')
    return scaled

traindf = pd.read_csv('traindf.csv')
n_train = traindf.shape[0]

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




'''
Load Saved Model
'''
import keras

with open('model-1.json', 'r') as myfile:
    loaded_model_json = myfile.readlines()[0]

from keras.models import model_from_json

loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model-1.h5")
print("Loaded model from disk")





'''
Evaluate loaded model on test data
'''
Adam = keras.optimizers.Adam(lr=0.0005, beta_1=0.95, beta_2=0.999, epsilon=0.00001, decay=0.00001, amsgrad=False)
loaded_model.compile(loss='mean_squared_error', optimizer=Adam)
score = loaded_model.evaluate([pic1, pic2], Y_train, verbose=1)
print('train loss', score)


pred = loaded_model.predict([pic1, pic2], verbose=1)
pred = pd.DataFrame(pred, columns = cols)




## get test validation data
testdf = pd.read_csv('testdf.csv')
n_test = testdf.shape[0]

Y_test = testdf.loc[:, cols]
for c in cols:
    Y_test[c] = pd.to_numeric(Y_test[c], errors='coerce').fillna(0)




print("Reading in images")
testpic1 = np.zeros(shape=(n_test, 600, 800, 3)) #.astype('int32')
testpic2 = np.zeros(shape=(n_test, 600, 800, 3)) #.astype('int32')
Rows = testdf.iterrows()
for i, row in tqdm(Rows):
    ## pic1
    img_path = row['BackLeft']
    img = imread(img_path)
    testpic1[i,:,:,:] = (img / 255).astype('float32')
    #testpic1[i,:,:,:] = scale(img/255)
    ## pic2
    img_path = row['BackRight']
    img = imread(img_path)
    testpic2[i,:,:,:] = (img / 255).astype('float32')
    #testpic2[i,:,:,:] = scale(img / 255)


score = loaded_model.evaluate([testpic1, testpic2], Y_test, verbose=1)
print('test loss', score)

test_pred = loaded_model.predict([testpic1, testpic2], verbose=1)
test_pred = pd.DataFrame(test_pred, columns = cols)
Y_test['Predicted Total'] = test_pred['Total']
Y_test.to_csv('Test_Results.csv', index=False)



#/home/jn107154/Pictures/Results/TestResults

#examples = np.random.randint(0, 792, 3)
for i in range(100):
    tmp_pred = test_pred.loc[i, 'Total']
    tmp_actual = Y_test.loc[i, 'Total']
    CaseID = testdf.loc[i, 'CaseID']
    title = 'CaseID: {} Delta V Actual : {} and Predicted: {}'.format(CaseID, tmp_actual, str(round(tmp_pred, 3)))
    fig = plt.figure(figsize=(25,15))
    img1 = testpic1[i]
    img2 = testpic2[i]
    plt.subplot(211)
    plt.imshow(img1)
    plt.title(title)
    plt.subplot(212)
    plt.imshow(img2)
    #fig.suptitle(title, size = 16)
    fig.tight_layout()
    plt.savefig('/home/jn107154/Pictures/NASS/Results/TestResults/Example {}.png'.format(i))
    plt.close()
    #plt.show()
    
