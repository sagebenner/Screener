# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imblearn
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
# Model performance
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from collections import Counter


#groups of surveys: 1 is just Brief, 2  includes items from other domains
survey = 1

#df = pd.read_csv('C:/Users/sageb/OneDrive - DePaul University/Documents/merged mouse data.csv')
#data = pd.read_csv(r"C:\Users\sageb\Documents\GitHub\Screener\MECFS No Comorbidities vs All Others3.csv")
data = pd.read_csv(r"C:\Users\sageb\Downloads\MECFS Controls F and S.csv")
#data = pd.read_csv(r"C:\Users\sageb\Downloads\MECFS vs Chronic F and S.csv")
#data= pd.read_csv(r"C:\Users\sageb\Downloads\CFS AND CHRONIC INCLUDED VS CONTROLS.csv")


df = data.drop(columns=('dx'))

pemdomain = ['minimum17', 'soreness15', 'heavy14', 'drained18', 'mental16', 'weakness33']
sleepdomain = ['unrefreshed19', 'nap20', 'falling21', 'staying22', 'early23', 'allday24']
cogdomain = ['remember36', 'attention37', 'word38', 'understanding39', 'focus40', 
             'unable41', 'slowness43', 'absent44']
paindomain = ['musclepain25', 'jointpain26', 'eyepain27', 'headaches31']
gastrodomain = ['bloating29', 'bowel46', 'stomach30', 'bladder45']
orthodomain = ['unsteady48', 'chestpain28', 'shortness49', 'dizz50', 'irregular51', 'nausea47']
circdomain = ['limbs56', 'hot58', 'ltemp60', 'sweating54', 'chills57', 'weight52', 'appetite53', 'night55']
immunedomain = ['flu65', 'fever64', 'lymphnodes63', 'sorethroat62', 'htemp59']
other = ['smells66', 'alcohol61', 'twitches32', 'noise34', 'lights35', 'depth42']

pemcount = []
sleepcount = []
cogcount = []

fatiguescore = [0] * len(data.index)
pemscore = [0] * len(data.index)
sleepscore = [0] * len(data.index)
cogscore = [0] * len(data.index)
painscore = [0] * len(data.index)
gastroscore = [0] * len(data.index)
orthoscore = [0] * len(data.index)
circscore = [0] * len(data.index)
immunescore = [0] * len(data.index)
otherscore = [0] * len(data.index)
diagnosis = [0] * len(data.index)

if survey == 1:
    for x in range(len(data.index)):
        if df['fatigue13f'][x] >= 2 and df['fatigue13s'][x] >= 2:
            fatiguescore[x] = 1
            '''
        if df['flu65f'][x] >= 1 and df['flu65s'][x] >= 1:
            immunescore[x] = 1
            '''
        for i in range(len(pemdomain)):
            if df[pemdomain[i] + 'f'][x] >= 2 and df[pemdomain[i] + 's'][x] >= 2:
                pemscore[x] = 1
                pemcount.append(pemdomain[i])
        for i in range(len(sleepdomain)):
            if df[sleepdomain[i] + 'f'][x] >= 1 and df[sleepdomain[i] + 's'][x] >= 1:
                sleepscore[x] = 1 
                sleepcount.append(sleepdomain[i])
        for i in range(len(cogdomain)):
            if df[cogdomain[i] + 'f'][x] >= 1 and df[cogdomain[i] + 's'][x] >= 1:
                cogscore[x] = 1 
                cogcount.append(cogdomain[i])
        if fatiguescore[x] ==1 and pemscore[x] == 1 and sleepscore[x] == 1 and \
            cogscore[x] ==1:
            diagnosis[x] = 1
            

        
    
    print(np.mean(diagnosis == data['dx']))
    print(pemcount)
    cf = confusion_matrix(data['dx'], diagnosis)
    pemcount = (Counter(pemcount))
    sleepcount = Counter(sleepcount)
    cogcount = Counter(cogcount)
    disp = ConfusionMatrixDisplay(cf)
    
    #disp.plot(xticks_rotation='vertical')
    #pem = plt.bar(pemcount.keys(), pemcount.values(), color='g')
    #sleep = plt.bar(sleepcount.keys(), sleepcount.values(), color='b')
    cog = plt.bar(cogcount.keys(), cogcount.values(), color='r')
    #pem.plot()
    #sleep.plot()
    #cog.plot()
    data['screen'] = diagnosis                

'''
df2 = data[(data['screen']==1)]

diagnosis2 = [0] * len(df2.index)
df2.reset_index(inplace=True)
for x in range(len(df2.index)):
    if df2['musclepain25f'][x] >= 2 and df2['musclepain25s'][x] >= 2:
        painscore[x] = 1     
    for i in range(1):
            if df2[gastrodomain[i] + 'f'][x] >= 2 and df2[gastrodomain[i] + 's'][x] >= 2:
                gastroscore[x] = 1 
    if df2['unsteady48f'][x] >= 2 and df2['unsteady48s'][x] >= 2:
        orthoscore[x] = 1                     
    for i in range(1):
            if df2[circdomain[i] + 'f'][x] >= 2 and df2[circdomain[i] + 's'][x] >= 2:
                circscore[x] = 1 
    if df2['flu65f'][x] >= 2 and df2['flu65s'][x] >= 2:
        immunescore[x] = 1   
    if df2['smells66f'][x] >= 2 and df2['smells66s'][x] >= 2:
        otherscore[x] = 1  
    if painscore[x]==1 and gastroscore[x]==1 and \
            orthoscore[x]==1 and circscore[x]==1 and immunescore[x]==1 and \
                otherscore[x]==1:
        diagnosis2[x] = 1

np.mean(diagnosis2 == df2['dx'])
'''    
if survey == 2:
        for x in range(len(data.index)):
            if df['fatigue13f'][x] >= 2 and df['fatigue13s'][x] >= 2:
                fatiguescore[x] = 1
            for i in range(len(pemdomain)):
                if df[pemdomain[i] + 'f'][x] >= 2 and df[pemdomain[i] + 's'][x] >= 2:
                    pemscore[x] = 1
            for i in range(len(sleepdomain)):
                    if df[sleepdomain[i] + 'f'][x] >= 2 and df[sleepdomain[i] + 's'][x] >= 2:
                        sleepscore[x] = 1 
            for i in range(len(cogdomain)):
                    if df[cogdomain[i] + 'f'][x] >= 2 and df[cogdomain[i] + 's'][x] >= 2:
                        cogscore[x] = 1  
                        
            for i in range(len(paindomain)):
                    if df[paindomain[i] + 'f'][x] >= 2 and df[paindomain[i] + 's'][x] >= 2:
                        painscore[x] = 1   
                        
            for i in range(len(gastrodomain)):
                    if df[gastrodomain[i] + 'f'][x] >= 2 and df[gastrodomain[i] + 's'][x] >= 2:
                        gastroscore[x] = 1 
                        
            for i in range(len(orthodomain)):
                    if df[orthodomain[i] + 'f'][x] >= 2 and df[orthodomain[i] + 's'][x] >= 2:
                        orthoscore[x] = 1 
                        
            for i in range(len(circdomain)):
                    if df[circdomain[i] + 'f'][x] >= 2 and df[circdomain[i] + 's'][x] >= 2:
                        circscore[x] = 1 
            for i in range(len(immunedomain)):
                    if df[immunedomain[i] + 'f'][x] >= 2 and df[immunedomain[i] + 's'][x] >= 2:
                        immunescore[x] = 1  
            for i in range(len(other)):
                    if df[other[i] + 'f'][x] >= 2 and df[other[i] + 's'][x] >= 2:
                        otherscore[x] = 1 
            if fatiguescore[x] ==1 and pemscore[x] == 1 and sleepscore[x] == 1 and \
                cogscore[x] ==1 and painscore[x]==1 and gastroscore[x]==1 and \
                    orthoscore[x]==1 and circscore[x]==1 and immunescore[x]==1 and \
                        otherscore[x]==1:
                diagnosis[x] = 1
    
        print(np.mean(diagnosis == data['dx']))
        
        cf = confusion_matrix(data['dx'], diagnosis)
        
        disp = ConfusionMatrixDisplay(cf)
        
        disp.plot(xticks_rotation='vertical')
        
        data['screen'] = diagnosis  
 
    
if survey == 3:
    for x in range(len(data.index)):                      
        for i in range(len(paindomain)):
            if df[paindomain[i] + 'f'][x] >= 2 and df[paindomain[i] + 's'][x] >= 2:
                painscore[x] = 1   
                print(i)
                        
        for i in range(len(gastrodomain)):
            if df[gastrodomain[i] + 'f'][x] >= 2 and df[gastrodomain[i] + 's'][x] >= 2:
                gastroscore[x] = 1 
                        
        for i in range(len(orthodomain)):
            if df[orthodomain[i] + 'f'][x] >= 1 and df[orthodomain[i] + 's'][x] >= 1:
                orthoscore[x] = 1 
                        
        for i in range(len(circdomain)):
            if df[circdomain[i] + 'f'][x] >= 2 and df[circdomain[i] + 's'][x] >= 2:
                circscore[x] = 1 
        for i in range(len(immunedomain)):
            if df[immunedomain[i] + 'f'][x] >= 1 and df[immunedomain[i] + 's'][x] >= 1:
                immunescore[x] = 1  
        for i in range(len(other)):
            if df[other[i] + 'f'][x] >= 1 and df[other[i] + 's'][x] >= 1:
                otherscore[x] = 1 
        if immunescore[x]==1 and orthoscore[x]==1 and\
                otherscore[x]==1:
                    diagnosis[x] = 1
        else:
            diagnosis[x]=0
    
print(np.mean(diagnosis == data['dx']))

cf = confusion_matrix(data['dx'], diagnosis)

disp = ConfusionMatrixDisplay(cf)

disp.plot(xticks_rotation='vertical')

data['screen'] = diagnosis  



