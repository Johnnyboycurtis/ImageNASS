import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## set seed
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



ind = np.random.rand(n) < 0.3


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




'''
Load Saved Model
'''

with open('model.json', 'r') as myfile:
    loaded_model_json = myfile.readlines()[0]

from keras.models import model_from_json

loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='mean_squared_error', optimizer='adadelta')
score = loaded_model.evaluate([pic1, pic2, pic3], Y_train, verbose=1)
print(score)
#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


pred = loaded_model.predict([pic1, pic2, pic3], verbose=1)
pred = pd.DataFrame(pred, columns = cols)





np.random.seed(5)
#examples = np.random.randint(0, 792, 3)
#examples = [372, 447, 775, 420, 206, 701, 118]
for i in examples:
    fig = plt.figure()
    img1 = pic1[i]
    img2 = pic2[i]
    img3 = pic3[i]
    plt.subplot(131)
    plt.imshow(img1)
    plt.subplot(132)
    plt.imshow(img2)
    plt.subplot(133)
    plt.imshow(img3)
    tmp_pred = pred.loc[i, 'Total']
    tmp_actual = Y_train.loc[i, 'Total']
    title = 'Delta V Actual : {} and Predicted: {}'.format(tmp_actual, str(round(tmp_pred, 3)))
    fig.suptitle(title, size = 16)
    #fig.subplots_adjust(top=0.88)
    fig.tight_layout()
    plt.savefig('/home/jn107154/Pictures/Results/Example {}.png'.format(i))
    plt.show()
    


## 372, 447, 775, 420, 206, 701, 118


fig = plt.figure(figsize=(10,30))
img1 = pic1[i]
img2 = pic2[i]
img3 = pic3[i]
plt.subplot(831)
plt.imshow(img1)
plt.subplot(832)
plt.imshow(img2)
plt.subplot(833)
plt.imshow(img3)
title = 'Delta V Actual : {} and Predicted: {}'.format(12, 9)
#plt.title(title)
fig.suptitle(title, size = 16)
fig.subplots_adjust(top=0.88)
fig.tight_layout()
plt.show()
plt.imsave()

