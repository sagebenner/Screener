# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 12:11:17 2023

@author: sbenner
"""
from pandas import *
import os
import numpy as np
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier  as rfc
from sklearn.datasets import make_classification
#import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.metrics import classification_report

from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler, NearMiss
from collections import Counter
from sklearn.tree import export_graphviz



dsqform = 1

path = "C:\\Users\\sbenner\\OneDrive - DePaul University\\Documents"
os.chdir(path)

df = read_csv("MECFS and COVID COMP.csv")
df2 = read_csv("MECFS CONTROLS 1.17.23 COMP.csv")
df3 = read_csv("MECFS vs chronic illness comp.csv")
df4 = read_csv('MECFS VS OTHERS BINARY.csv')

df4 = df2

labels = np.array(df4['dx'])

features = df4.drop(columns='dx')

if dsqform==1:
    features = features[['fatigue13c', 'minimum17c', 'unrefreshed19c', 'remember36c']]

feature_list = list(features.columns)

features = np.array(features)

train_features, test_features, train_labels, test_labels= tts(features, labels, test_size=0.25, random_state=42)

rf = rfc(n_estimators = 1000, random_state=42)

rf.fit(train_features, train_labels)

predictions = rf.predict(test_features)

errors = abs(predictions - test_labels)

print('Mean absolute error:', round(np.mean(errors), 2))




ros = RandomOverSampler(random_state=42)

features_train_ros, labels_train_ros = ros.fit_resample(train_features, train_labels)

print(sorted(Counter(labels_train_ros).items()))

rf2 = rfc(n_estimators=1000, random_state=42)
rf2.fit(features_train_ros, labels_train_ros)

predictions2=rf2.predict(test_features)
accuracy = np.mean(predictions2==test_labels)
print('Model accuracy: ', round(accuracy, 2))



#sns.stripplot(x='fatigue13c', y = 'minimum17c', hue = 'dx', data = df2)

