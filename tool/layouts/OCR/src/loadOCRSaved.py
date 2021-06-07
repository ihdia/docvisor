import sys
import os
import json
import numpy as np
# print(sys.argv)

if len(sys.argv)<2:
    print('Wrong format')



def parseOCRJson(dataPath):
    with open(dataPath,'r') as dataFile:
        data = json.load(dataFile)
    return data


def loadData(saveDir):
    allData = {}
    reqdData = {}
    with open(saveDir+'/'+'save.txt') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    data = [tuple(x.split()) for x in lines]
    data = set(data)
    # print(data)

    for doc in data:
        docClass , index = doc
        index = int(index)
        if docClass not in allData:
            allData[docClass] = parseOCRJson(saveDir+'/'+docClass+'.json')
        
        if docClass not in reqdData:
            reqdData[docClass] = []
        
        reqdData[docClass].append(allData[docClass][index])

    return reqdData

completeData = {}

dirsOI = sys.argv[2:-2]
layout = sys.argv[-2]
pageName = sys.argv[-1]

pathPrefix = sys.argv[1]
for diR in dirsOI:
    saveDir = pathPrefix+'/'+diR+'/'+layout+'/'+pageName
    dirData = loadData(saveDir)

    for docClass in dirData:
        if docClass not in completeData:
            completeData[docClass] = []
        
        completeData[docClass]+=dirData[docClass]

for docClass in completeData:
    wdata = completeData[docClass]
    with open(f'{docClass}_saved.json','w') as write_file:
        json.dump(wdata, write_file, indent=4)

# python script pathtosavedir 0 1 2 3 OCR Handwritten