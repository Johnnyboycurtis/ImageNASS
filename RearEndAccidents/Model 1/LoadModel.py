import os
os.chdir('/home/jn107154/Documents/ImageNASS/RearEndAccidents/Model 1')
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## set seed
np.random.seed(123546789)


def update_names(imgpath):
    pictures = '/home/jn107154/Pictures/NASS'
    img_name = imgpath.split('/')[-1]
    caseid = imgpath.split('/')[-2]
    new_path = os.path.join(pictures, caseid, 'resized', img_name)
    return new_path


InputDF = pd.read_csv('InputDF.csv', dtype={'CaseID':str})  ## has old paths

back_end_ = pd.read_csv("../Back_End.csv", dtype={'CaseID':str, 'VehicleNumber':str}, na_values='Unknown')
back_end_.head()

rear_events = pd.read_csv('../rear_events.csv', dtype={'CaseID':str, 'VehicleNumber':str, 'ContactedVehicleNumber':str}, na_values='Unknown')
rear_events.head()

back_end_events = pd.merge(left = back_end_, right = rear_events, on = ['CaseID', 'VehicleNumber'])


df = pd.merge(left=back_end_events, right = InputDF, on = 'CaseID')
df = df.sample(frac=1).reset_index(drop=True)


df['BackLeft'] = df['BackLeft'].map(update_names)
df['BackRight'] = df['BackRight'].map(update_names)

ind = ~df.Total.isnull().values
df = df.loc[ind]
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




'''
Load Saved Model
'''

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
loaded_model.compile(loss='mean_squared_error', optimizer='adadelta')
score = loaded_model.evaluate([pic1, pic2], Y_train, verbose=1)
print(score)
#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


pred = loaded_model.predict([pic1, pic2], verbose=1)
pred = pd.DataFrame(pred, columns = cols)






testdf = df.loc[~ind].reset_index(drop=False).loc[:100]
n_test = testdf.shape[0]

Y_test = testdf.loc[:, cols]
for c in cols:
    Y_test[c] = pd.to_numeric(Y_test[c], errors='coerce').fillna(0)




print("Reading in images")
testpic1 = np.zeros(shape=(n_test, 600, 800, 3)) #.astype('int32')
testpic2 = np.zeros(shape=(n_test, 600, 800, 3)) #.astype('int32')
for i, row in testdf.iterrows():
    ## pic1
    img_path = row['BackLeft']
    img = imread(img_path)
    testpic1[i,:,:,:] = (img / 255).astype('float32')
    ## pic2
    img_path = row['BackRight']
    img = imread(img_path)
    testpic2[i,:,:,:] = (img / 255).astype('float32')


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
    plt.subplot(213)
    plt.imshow(img3)
    #fig.suptitle(title, size = 16)
    fig.tight_layout()
    plt.savefig('/home/jn107154/Pictures/NASS/Results/TestResults/Example {}.png'.format(i))
    plt.close()
    #plt.show()
    


testdf.loc[[26,45]] ## this is a mistake; pictures do not match the CaseID
#https://crashviewer.nhtsa.dot.gov/nass-cds/CaseForm.aspx?xsl=main.xsl&CaseID=785014352
#https://crashviewer.nhtsa.dot.gov/nass-cds/CaseForm.aspx?xsl=main.xsl&CaseID=762013184

