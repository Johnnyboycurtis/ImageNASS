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
df = df.sample(frac=1).reset_index(drop=True) ## shuffling the data

df['BackLeft'] = df['BackLeft'].map(update_names)
df['BackRight'] = df['BackRight'].map(update_names)

ind = ~df.Total.isnull().values
df = df.loc[ind]
n = df.shape[0]
print('Number of Records', n)

CaseID = df.CaseID.unique()
n_cases  = CaseID.shape[0]
ind = np.random.rand(n_cases) < 0.88

train_caseid = CaseID[ind]

test_caseid = CaseID[~ind]

def not_in_questionable(caseid):
    'Questionable CaseIDs'
    questionable = ['835016743']
    return caseid not in questionable

def in_training(caseid):
    return caseid in train_caseid

ind = df.CaseID.apply(in_training)
q_ind = df.CaseID.apply(not_in_questionable)



traindf = df.loc[ind & q_ind].reset_index(drop=False)
n_train = traindf.shape[0]
print('Number of Training Records', n_train)

traindf.to_csv('traindf.csv', index=False)




testdf = df.loc[~ind & q_ind].reset_index(drop=False)
n_test = testdf.shape[0]
print('Number of Test Records', n_test)

testdf.to_csv('testdf.csv', index=False)


