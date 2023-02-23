# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 14:10:11 2023

@author: sbenner
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imblearn
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
# Model performance
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as pyo

pemdomain = ['minimum17f', 'soreness15f', 'drained18f', 'mental16f', 'heavy14f', 'weakness33f',
             'minimum17s', 'soreness15s', 'drained18s', 'mental16s', 'heavy14s', 'weakness33s']


sleepdomain = ['unrefreshed19f', 'nap20f', 'falling21f', 'staying22f', 'early23f', 'allday24f',
               'unrefreshed19s', 'nap20s', 'falling21s', 'staying22s', 'early23s', 'allday24s']

cogdomain = ['remember36f', 'difficulty37f', 'word38f', 'absent44f', 'focus40f','slowness43f','understanding39f', 'unable41f',
             'remember36s', 'difficulty37s', 'word38s', 'absent44s', 'focus40s','slowness43s','understanding39s', 'unable41s']

paindomain = ['musclepain25f', 'jointpain26f', 'eyepain27f', 'headaches31s',
              'musclepain25s', 'jointpain26s', 'eyepain27s', 'headaches31f']


gastrodomain = ['bloating29f', 'bowel46f', 'stomach30f', 'bladder45f',
                'bloating29s', 'bowel46s', 'stomach30s', 'bladder45s']

orthodomain = ['unsteady48f', 'chestpain28f', 'shortness49f', 'dizz50f', 'irregular51f', 'nausea47f',
               'unsteady48s', 'chestpain28s', 'shortness49s', 'dizz50s', 'irregular51s', 'nausea47s']

circdomain = ['limbs56f', 'hot58f', 'ltemp60f', 'sweating54f', 'chills57f', 'weight52f', 'appetite53f', 'night55f',
              'limbs56s', 'hot58s', 'ltemp60s', 'sweating54s', 'chills57s', 'weight52s', 'appetite53s', 'night55s']

immunedomain = ['flu65f', 'fever64f', 'lymphnodes63f', 'sorethroat62f', 'htemp59f',
                'flu65s', 'fever64s', 'lymphnodes63s', 'sorethroat62s', 'htemp59s']

neuroendomain = ['smells66f', 'alcohol61f', 'twitches32f', 'noise34f', 'lights35f', 'depth42f',
         'smells66s', 'alcohol61s', 'twitches32s', 'noise34s', 'lights35s', 'depth42s']

#Maybe change this to the imputed data:
df = pd.read_csv('MECFS and Controls F+S Reduction.csv')

df['fatigue'] = np.mean(df[['fatigue13f', 'fatigue13s']], axis=1)
df['pemmean'] = np.mean(df[pemdomain], axis=1)
df['sleepmean'] = np.mean(df[sleepdomain], axis=1)
df['cogmean'] = np.mean(df[cogdomain], axis=1)
df['painmean'] = np.mean(df[paindomain], axis=1)
df['gastromean'] = np.mean(df[gastrodomain], axis=1)
df['orthomean'] = np.mean(df[orthodomain], axis=1)
df['circmean'] = np.mean(df[circdomain], axis=1)
df['immunemean'] = np.mean(df[immunedomain], axis=1)
df['neuroendomain'] = np.mean(df[neuroendomain], axis=1)

'''
test = df.iloc[:, 110:119]
test2 = np.mean(test, axis=0)

cfs = df[(df['dx']==1)]
cfsdomain = np.mean(cfs.iloc[:, 110:120], axis=0)

test3 = np.array(cfsdomain[:])

categories = ['Fatigue', 'PEM', 'Sleep', 'Cognitive Problems', 'Pain', 'Gastro Problems',
                  'Orthostatic Intolerance', 'Circulatory Problems', 'Immune System', 'Neuroendocrine Problems']

fig = go.Figure(
        data=[
            go.Bar(y=cfsdomain)])

pyo.plot(fig)
'''