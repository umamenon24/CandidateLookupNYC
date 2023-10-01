

import json
import re

f1 = open("dataMAIN.csv", "r")
f2=open("dataIE.csv", "r")
f3=open('dataISET.csv', 'r')
dictionary =[]

lines0=f3.readlines()
issues=[elem[:-1] for elem in lines0]

f3.close()

# fullData=[]
# parties=["D", "R", "WF", "C", "MF"]

lines = f1.readlines()
lines=[line[:-1] for line in lines]
lines=[line.split(',',4) for line in lines]

lines1=f2.readlines()
lines1=[line[:-1] for line in lines1]
#print(lines)
for elem in lines:
    dictionary.append({
        "name": elem[0],
        "district": elem[1]
    })
    currentKey=dictionary[lines.index(elem)]

    currentKey["district"]=elem[1]
    if "," in elem[4]:
        currentKey["party"]=elem[4].split(',')
        currentKey["party"][0]=currentKey["party"][0][1:]
        currentKey["party"][1]=currentKey["party"][1][1:-1]
    else:
        currentKey["party"]=elem[4]
    currentKey["ic"]=elem[2]
    
    if '"' in lines1[lines.index(elem)]:
        x=lines1[lines.index(elem)].split('",')
        x[0]=x[0][1:]
        currentKey['issues']=x[0].split(', ')
        if '"' in x[1]: 
            x[1]=x[1][1:-1]
            currentKey['endorsements']=x[1].split(', ')
        else: currentKey['endorsements']=lines1[lines.index(elem)].split(', ')[1]
    else: 
        currentKey['issues']=lines1[lines.index(elem)].split(',')[0]
        currentKey['endorsements']=lines1[lines.index(elem)].split(',')[1]
   
    currentKey['website']=elem[3]
    
f1.close()
f2.close()


f4 = open("data.json", "w")
json.dump(dictionary, f4, indent = 4)
f4.close()