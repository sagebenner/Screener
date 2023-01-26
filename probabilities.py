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


fatiguescore = 2.5
minexscore = 1.5
sleepscore = 2.0
cogscore = 3.0


pmecfs = (mecfs['fatigue13c'].value_counts(normalize=True) ).reset_index(level=0)
pother = (others['fatigue13c'].value_counts(normalize=True)).reset_index(level=0)



probcfs = pmecfs.fatigue13c[(pmecfs["index"]>=fatiguescore)]
probcfs = np.sum(probcfs)
probnotcfs = pmecfs.fatigue13c[(pmecfs["index"]<fatiguescore)]
probnotcfs = np.sum(probnotcfs)

totalprob = probcfs + probnotcfs

probother = pother.fatigue13c[(pother['index']<=fatiguescore)]
probother = np.sum(probother)

test = totalprob * probother

(df4.dx==1).mean()
(df4.query("fatigue13c >= @fatiguescore")).mean()
probablyME = (df4.query("fatigue13c == @fatiguescore")['dx']==1).mean()

probablyOther = (df4.query("fatigue13c == @fatiguescore")['dx']==0).mean()




(df4.query("dx")['fatigue13c'] >= fatiguescore).mean()
