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
import seaborn as sns
from sklearn.metrics import classification_report

from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler, NearMiss
from collections import Counter
from sklearn.tree import export_graphviz
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV

dsqform = 2

path = "C:\\Users\\sbenner\\OneDrive - DePaul University\\Documents"
os.chdir(path)

#df = read_csv("MECFS and COVID COMP.csv")
#df2 = read_csv("MECFS CONTROLS 1.17.23 COMP.csv")
#df3 = read_csv("MECFS vs chronic illness comp.csv")
df4 = read_csv('MECFS VS OTHERS BINARY.csv')

#df4 = df2

labels = np.array(df4['dx'])

features = df4.drop(columns='dx')

features2 = features[['fatigue13c', 'soreness15c', 'minimum17c', 
                         'unrefreshed19c', 'musclepain25c', 'bloating29c',
                         'remember36c', 'difficulty37c', 'bowel46c',
                         'unsteady48c', 'limbs56c', 'hot58c', 'flu65c', 'smells66c' ]]

features = features[['fatigue13c', 'minimum17c', 'unrefreshed19c', 'remember36c']]


#Brief screener version:
feature_list = list(features.columns)

features = np.array(features)

train_features, test_features, train_labels, test_labels= tts(features, labels, test_size=0.25, random_state=42)

ros = RandomOverSampler(random_state=42)

features_train_ros, labels_train_ros = ros.fit_resample(train_features, train_labels)

print(sorted(Counter(labels_train_ros).items()))

rf = rfc(max_depth=16, max_features=None, max_leaf_nodes=59)
rf = rfc()
rf.fit(features_train_ros, labels_train_ros)

predictions=rf.predict(test_features)
accuracy = accuracy_score(test_labels, predictions)
print(accuracy)
print(confusion_matrix(test_labels, predictions))

#Short form 14 version:
feature_list2 = list(features2.columns)
features2 = np.array(features2)
train_features2, test_features2, train_labels2, test_labels2= tts(features2, labels, test_size=0.25, random_state=42)

ros = RandomOverSampler(random_state=42)

features_train_ros2, labels_train_ros2 = ros.fit_resample(train_features2, train_labels2)

rf2 = rfc(max_depth=16, max_features=None, max_leaf_nodes=59)
rf2 = rfc()
rf2.fit(features_train_ros2, labels_train_ros2)

predictions2=rf2.predict(test_features2)
accuracy2 = accuracy_score(test_labels2, predictions2)
print(accuracy2)
print(confusion_matrix(test_labels2, predictions2))
#rf = rfc(n_estimators = 1000)

#rf.fit(train_features, train_labels)

#predictions = rf.predict(test_features)

#errors = abs(predictions - test_labels)

#print('Mean absolute error:', round(np.mean(errors), 2))





#print('Model accuracy: ', round(accuracy, 2))

param_grid = {
    'n_estimators': [25, 50, 100, 150, 900, 2000],
    'max_features': ['sqrt', 'log2', None],
    'max_depth': [3, 6, 9, 16, 70, 500],
    'max_leaf_nodes': [3, 6, 9, 14, 59],
}

#grid_search = GridSearchCV(rfc(), param_grid= param_grid)

#grid_search.fit(features_train_ros, labels_train_ros)
#print(grid_search.best_estimator_)

#sns.stripplot(x='fatigue13c', y = 'minimum17c', hue = 'dx', data = df2)

