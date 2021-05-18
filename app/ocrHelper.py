import json
import numpy as np
from PIL import Image,ImageOps
import matplotlib.pyplot as plt
import cv2 as cv
import os


class OCRInputError(Exception):
    pass

class OCRHelper:

    def __init__(self,jsonFilePath):

        if not os.path.exists(jsonFilePath):
            raise OCRInputError

        self.jsonFilePath = jsonFilePath

        # load data:

        self.JSONdata = self.loadOCRData(self.jsonFilePath)

        self.len = len(self.JSONdata)

        self.metrics = list(self.JSONdata[0]["metrics"].keys())

        

        self.sortedSecIndices = {}

        self.sortedSecIndices['None'] = [i for i in range(len(self.JSONdata))]

        for metric in self.metrics:
            self.sortedSecIndices[metric]= [i[0] for i in sorted(enumerate(self.JSONdata), key=lambda x:x[1]['metrics'][metric])]
    
        self.metrics.append("None")
    
    def parseOCRJson(self,dataPath):
        with open(dataPath,'r') as dataFile:
            data = json.load(dataFile)
        return data
    
    def getData(self,index):
        return self.JSONdata[index]
    
    def loadOCRData(self,dataPath):
        data = self.parseOCRJson(dataPath)

        # manipulate the attentions:

        for i in range(len(data)):
            data[i]["attentions"] = np.array(data[i]["attentions"]).reshape((-1,2))

        return data
    
    def loadImage(self,idx,data):

        imagePath = data[idx]["imagePath"]

        try:
            im = Image.open(imagePath)
        except:
            print(f'No Image with path {imagePath} found')
        
        im = ImageOps.grayscale(im)
        img_data = np.asarray(im, dtype=np.uint8)

        data[idx]["image"] = im

        return img_data
    
    def setCharLevelAtts(self,idx,data):

        san_pred = data[idx]["annotation"]["prediction"]

        charLevelAtts = []
        start = 0
        end = 0
        atts = data[idx]["attentions"]
        # try:

        for i in range(len(san_pred)):
            loi = len(str(ord(san_pred[i])))
            end = start+loi
            # print(end,atts.shape)
            if end >= atts.shape[0]:
                end = atts.shape[0]-1
            chStart = atts[start][0]
            chEnd = atts[end][1]

            charLevelAtts.append([chStart,chEnd])
            start = end
        
        data[idx]["charLevelAtts"] = charLevelAtts
        
        # except:
        #     print('Some error in setting the CharLevelAttentions')
        
    
    def highlightImage(self,idx,start,end,data,hcolor="#00FFFF"):

        getRGB = lambda x : tuple(int(x[i:i+2], 16) for i in (0, 2, 4))

        rgbtuple = getRGB(hcolor.lstrip("#"))

        
        # accounting for backward mouse selection:
        if start > end:
            temp = start
            start = end
            end = start
        
        # load image if not already loaded:

        if "image" not in data[idx]:
            imageData = self.loadImage(idx,data)
        
        else:

            im = ImageOps.grayscale(data[idx]["image"])
            imageData = np.asarray(im, dtype=np.uint8)
        

        # return plain image on no selection
        if start==end:
            return imageData

        
        # if charLevelAttentions are not calculated, calculate them:
        
        try:
            atts = data[idx]["charLevelAtts"]

        except:
            self.setCharLevelAtts(idx,data)
            try:
                atts =  data[idx]["charLevelAtts"]
            except:
                print('Some Issue with attentions')
                return -1

        
        # load your image_array:
        
        hImage = np.copy(imageData)
        hImage2 = np.copy(imageData)
        if len(hImage.shape)< 3:
            hImage = cv.cvtColor(hImage, cv.COLOR_GRAY2RGB)
            hImage2 = cv.cvtColor(hImage2, cv.COLOR_GRAY2RGB)

        try:
            b, g, r = cv.split(hImage)
            mask = (b > 50) & (g > 50) & (r > 50)
            hImage[mask]= rgbtuple
            hImage2[:,atts[start][0]:atts[end][1],:] = hImage[:,atts[start][0]:atts[end][1],:]
        except IndexError:
            hImage[:,atts[start][0]:atts[len(data[idx]["annotation"]["prediction"])-1][1],0] = rgbtuple

        return hImage2
    
    def getText(self,idx,start,end,data):

    

        try:
            mapping = data[idx]["charLevelAtts"]

        except:
            self.setCharLevelAtts(idx,data)
            try:
                mapping =  data[idx]["charLevelAtts"]
            except:
                print('Some Issue with attentions')
                return -1
        

        if start == -1 and end == -1:
            return [{'start': -1, 'end': -1}]
        
        startIdx = -1
        endIdx = -1

        # print(start,end)

        itLeng = len(mapping)

        for i in range(itLeng):
            s,e = mapping[i]
            if startIdx==-1:
                if start in range(s,e+1):
                    startIdx = i
            if end in range(s,e+1):
                endIdx = i
        
        if end > e:
            endIdx = itLeng

        # print(mapping)
                
        return [{'start': startIdx, 'end': endIdx}]
        
