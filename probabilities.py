# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:44:58 2023

@author: sbenner
"""
import statistics
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

path = "C:\\Users\\sbenner\\OneDrive - DePaul University\\Documents"
os.chdir(path)

df = read_csv("MECFS and COVID COMP.csv")
df2 = read_csv("MECFS CONTROLS 1.17.23 COMP.csv")
df3 = read_csv("MECFS vs chronic illness comp.csv")
df4 = read_csv('MECFS VS OTHERS BINARY.csv')

mecfs = df[(df["dx"]==1)]

others = df4[(df4["dx"]==0)]


fatiguescore = 4
pemscore = 1
sleepscore = 1
cogscore = 1


pmecfs = (mecfs['fatigue13c'].value_counts(normalize=True) ).reset_index(level=0)
pother = (others['fatigue13c'].value_counts(normalize=True)).reset_index(level=0)



probcfs = pmecfs.fatigue13c[(pmecfs["index"]<=fatiguescore)]
probcfs = np.sum(probcfs)
probnotcfs = pother.fatigue13c[(pmecfs["index"]>=fatiguescore)]
probnotcfs = np.sum(probnotcfs)

totalprob = probcfs + probnotcfs

testprob = 1-probcfs

testprob2 = 1-probnotcfs

probother = pother.fatigue13c[(pother['index']<=fatiguescore)]
probother = np.sum(probother)

test = totalprob * probother

(df4.dx==1).mean()
(df4.query("fatigue13c >= @fatiguescore")).mean()
probablyME = (df4.query("fatigue13c == @fatiguescore & minimum17c == @pemscore & unrefreshed19c == @sleepscore & remember36c == @cogscore")['dx']==1).mean()
probablyME = (df4.query("fatigue13c == @fatiguescore & minimum17c == @pemscore")['dx']==1).mean()

test = df4[(df4.fatigue13c == fatiguescore)]

print(f"Your probability of having ME/CFS is {probablyME}")

newdf = df4[(df4.fatigue13c == fatiguescore) & (df4.minimum17c == pemscore) & (df4.unrefreshed19c == sleepscore) & (df4.remember36c == cogscore)]

probablyME2 = (df4.query("minimum17c == @pemscore")['dx']==1).mean()
probablyME3 = (df4.query("fatigue13c == @fatiguescore")['dx']==1).mean()
probablyME4 = (df4.query("unrefreshed19c == @sleepscore")['dx']==1).mean()
probablyME5 = (df4.query("remember36c == @cogscore")['dx']==1).mean()
test = (probablyME3+probablyME2+probablyME4+probablyME5)/4

probablyOther = (df4.query("fatigue13c == @fatiguescore")['dx']==0).mean()
probablyOther2 = (df4.query("minimum17c == @pemscore")['dx']==0).mean()

test2 = (probablyME3 + probablyME2) - probablyOther - probablyOther2

burden = df4.iloc[0,4]
burden = np.sum([df4.iloc[4,1:55]])
burden = list()
for x in range(len(df4.index)):
    burden.append(np.sum([df4.iloc[x,1:55]]))
