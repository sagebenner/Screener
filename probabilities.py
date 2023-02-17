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
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report

from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler, NearMiss
from collections import Counter
from sklearn.tree import export_graphviz
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo

path = "C:\\Users\\sbenner\\OneDrive - DePaul University\\Documents"
os.chdir(path)


#Define whether we use qcut method or cut method manually
q_cut = 0


df = read_csv("MECFS and COVID COMP.csv")
df2 = read_csv("MECFS CONTROLS 1.17.23 COMP.csv")
df3 = read_csv("MECFS vs chronic illness comp.csv")
df4 = read_csv('MECFS VS OTHERS BINARY.csv')


mecfs = df[(df["dx"]==1)]

others = df4[(df4["dx"]==0)]

controls = df2[(df2['dx']==0)]

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

#Working on categories for probability calculations


responses = [4,4,4,4]

# qcut automatically creates bins, approximately equal sized. .rank "first" method forces equal sized bins
qfatigue, fatiguebins = qcut(df4['fatigue13c'], q=2, labels=['low', 'high'], retbins=True)
qminex, minexbins = qcut(df4['minimum17c'], q=2, labels=['low', 'high'], retbins=True)
qunrefresh, unrefreshbins = qcut(df4['unrefreshed19c'], q=2, labels=['low', 'high'], retbins=True)
qremember, rememberbins = qcut(df4['remember36c'], q=2, labels=['low', 'high'], retbins=True)



if q_cut == 0:
    bins = [-np.inf, 1.9, 2.9, np.inf]
    labels = ['low', 'mid','high']
    qfatigue = cut(x=df4['fatigue13c'], bins = bins, labels=labels, right = True)
    qminex = cut(x=df4['minimum17c'], bins = bins, labels=labels, right = True)
    qunrefresh = cut(x=df4['unrefreshed19c'], bins = bins, labels=labels, right = True)
    qremember = cut(x=df4['remember36c'], bins = bins, labels=labels, right = True)
    
df4['qfatigue'] = qfatigue
df4['qminex'] = qminex
df4['qunrefresh'] = qunrefresh
df4['qremember'] = qremember

def binAccuracy(newrow, df4):
    add = []
    binList = [fatiguebins, minexbins, unrefreshbins, rememberbins]
    for y in range(len(newrow)):
        score = np.array([newrow[y]])
        binVal = cut(score, bins=bins, labels=labels, right=True).astype('str')
        add.append(binVal[0])
    sample_size = (df4.query(f"qfatigue == '{add[0]}' & qminex == '{add[1]}' & qunrefresh == '{add[2]}' & qremember == '{add[3]}'")['dx']==1)
    return sample_size

#sample_size = (df4.query(f"qfatigue == '{add[0]}' & qminex == '{add[1]}' & qunrefresh == '{add[2]}' & qremember == '{add[3]}'")['dx']==1)

test = binAccuracy(responses, df4).mean()

test = df4[(df4['fatigue13c'] >= (responses[0]-0.5)) & 
           (df4['fatigue13c'] <= (responses[0] + 0.5)) &
           (df4['minimum17c'] >= (responses[1] - 0.5)) &
           (df4['minimum17c'] <= (responses[1] + 0.5)) & 
           (df4['unrefreshed19c'] >= (responses[2] - 0.5)) &
           (df4['unrefreshed19c'] <= (responses[2] + 0.5)) &
           (df4['remember36c'] <= (responses[3] + 0.5)) &
           (df4['remember36c'] >= (responses[3] - 0.5))] 

np.mean(test['dx']==1)


# I'm going to test the dsq-sf for the probabilities method
data = [2,2,2,2,2,2,2,2,2,2,2,2,2,2]
df = df4
newdf = df[(df['fatigue13c'] >= (data[0]-1)) &
                (df['fatigue13c'] <= (data[0] + 1)) &
                (df['soreness15c'] >= (data[1] - 1)) &
                (df['soreness15c'] <= (data[1] + 1)) &
                (df['minimum17c'] >= (data[2] - 1)) &
                (df['minimum17c'] <= (data[2] + 1)) &
                (df['unrefreshed19c'] >= (data[3] - 1)) &
                (df['unrefreshed19c'] <= (data[3] + 1)) &
                (df['musclepain25c'] >= (data[4] - 1)) &
                (df['musclepain25c'] <= (data[4] + 1)) &
                (df['bloating29c'] >= (data[5] - 1)) &
                (df['bloating29c'] <= (data[5] + 1)) &
                (df['remember36c'] <= (data[6] + 1)) &
                (df['remember36c'] >= (data[6] - 1)) &
                (df['difficulty37c'] >= (data[7] - 1)) &
                (df['difficulty37c'] <= (data[7] + 1)) &
                (df['bowel46c'] >= (data[8] - 1)) &
                (df['bowel46c'] <= (data[8] + 1)) &
                (df['unsteady48c'] >= (data[9] - 1)) &
                (df['unsteady48c'] <= (data[9] + 1)) &
                (df['limbs56c'] >= (data[10] - 1)) &
                (df['limbs56c'] <= (data[10] + 1)) &
                (df['hot58c'] >= (data[11] - 1)) &
                (df['hot58c'] <= (data[11] + 1)) &
                (df['flu65c'] >= (data[12] - 1)) &
                (df['flu65c'] <= (data[12] + 1)) &
                (df['smells66c'] >= (data[13] - 1)) &
                (df['smells66c'] <= (data[13] + 1))]

sample_size = len(newdf.index)
testAcc = np.mean(newdf['dx'] == 1).round(decimals=2) * 100


#test = cut(responses[0:,1], bins=fatiguebins, labels=['low', 'mid', 'high']).astype('str')


#(df4.query(f"qfatigue == '{add[0]}' & qminex == '{add[1]}' & qunrefresh == '{add[2]}' & qremember == '{add[3]}'")['dx']==1).mean()

#plotting histograms of each bin, separated by dx 
#plt.hist(df4.qfatigue[(df4['dx']==1)])

#plt.hist(df4.qfatigue[(df4['dx']==0)])

crosstab(df4.qfatigue, df4.dx).plot(kind='bar')

crosstab(df4.qminex, df4.dx).plot(kind='bar')

crosstab(df4.qunrefresh, df4.dx).plot(kind='bar')

crosstab(df4.qremember, df4.dx).plot(kind='bar')

#Working on radar plot
newdf = mecfs.drop(columns='dx')

"""features2 = features[['fatigue13c', 'soreness15c', 'minimum17c', 
                         'unrefreshed19c', 'musclepain25c', 'bloating29c',
                         'remember36c', 'difficulty37c', 'bowel46c',
                         'unsteady48c', 'limbs56c', 'hot58c', 'flu65c', 'smells66c' ]]"""

newdf = newdf[['fatigue13c', 'minimum17c', 'unrefreshed19c', 'remember36c']]

fatmean = np.mean([newdf['fatigue13c']])
minmean = np.mean([newdf['minimum17c']])
sleepmean = np.mean([newdf['unrefreshed19c']])
cogmean = np.mean([newdf['remember36c']])

combmean = [fatmean, minmean, sleepmean, cogmean]

othermean = [np.mean([others['fatigue13c']]), np.mean([others['minimum17c']]), np.mean([others['unrefreshed19c']]), np.mean([others['remember36c']])]

controlmean = [np.mean([controls['fatigue13c']]), np.mean([controls['minimum17c']]), np.mean([controls['unrefreshed19c']]), np.mean([controls['remember36c']])]

feature_list = np.array(newdf.columns)
categories = [*feature_list, feature_list[0]]
#features = np.array(features)

responses = [2, 3, 2, 3]

label_loc = np.linspace(start = 0, stop = 2 * np.pi, num=len(responses))

testdf = mecfs.mean(axis=0)

testintersect = df2[df2.columns.intersection(newdf.columns)]

shortform_items = ['fatigue13c', 'soreness15c', 'minimum17c', 'unrefreshed19c',
                   'musclepain25c', 'bloating29c', 'remember36c', 'difficulty37c',
                   'bowel46c', 'unsteady48c', 'limbs56c', 'hot58c', 'flu65c', 
                   'smells66c']

dsqsf = df4[shortform_items]
'''
fig = go.Figure(
    data=[
        go.Scatterpolar(r=othermean, theta=categories, fill='toself', name = "Average Healthy Control scores"),
        go.Scatterpolar(r=combmean, theta=categories, fill='toself', name = "Average ME/CFS scores"),
        go.Scatterpolar(r=responses, theta=categories, fill='toself', name = "Your scores")], 
        layout=go.Layout(
        title=go.layout.Title(text='Score comparison'),
        polar={'radialaxis': {'visible': True}},
        showlegend = True))
fig.update_polars(radialaxis=dict(range=[0, 4]))

pyo.plot(fig, include_plotlyjs=False, output_type='div')


fig.write_image("figure.png")variable = 'fatigue13c'

lowfat = df4.query(f'{variable} >=0 & {variable} <= 1')
midlowfat = df4.query(f'{variable} >1 & {variable} <= 2')
medfat = df4.query(f'{variable} > 2 & {variable} <=3')
hifat = df4.query(f'{variable} > 3 & {variable} <=4')
(hifat['dx']==1).mean()

df4['test'] = cut(x=df4['fatigue13c'], bins = [0,  2, np.inf], labels=['low', 'high'], right = False)



'''