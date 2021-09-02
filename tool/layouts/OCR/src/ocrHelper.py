import json
import numpy as np
from PIL import Image,ImageOps
import matplotlib.pyplot as plt
import cv2 as cv
import os
import streamlit as st


class OCRInputError(Exception):
    pass

class OCRHelper:

    def __init__(self,jsonFilePath,isDataLatex=False):

        self.isDataLatex = isDataLatex

        if not os.path.exists(jsonFilePath):
            # print(jsonFilePath)
            raise OCRInputError

        # valid json file path
        self.jsonFilePath = jsonFilePath

        # load data:
        self.JSONdata = self.loadOCRData(self.jsonFilePath)


        # calculate and store the length of the data for easy retrieval
        self.len = len(self.JSONdata)

        # our code assumes uniformity in the whole data.
        # by uniformity we mean that if your json file has 
        # whatever minimum is required to load the tool 
        # in the format specified in the documentation, we can load the app,
        # however we assume that the data itself is uniform i.e. whatever keys are there in the first
        # dictionary will be there in all the dictionaries of the data array.

        self.isAtleastSingleAttentionModelPresent = False

        if 'outputs' in self.JSONdata[0]:

            self.models = list(self.JSONdata[0]['outputs'].keys())
            self.no_ocr_models = len(self.models)
            

            self.attentionModelIndexes = []

            for i in range(self.no_ocr_models):
                model = self.models[i]

                if not self.isDataLatex and "attentions" in self.JSONdata[0]['outputs'][model]:
                    self.isAtleastSingleAttentionModelPresent =True
                    self.attentionModelIndexes.append(i)

            if self.isAtleastSingleAttentionModelPresent:
                
                re_arranged_models = []

                for idx in self.attentionModelIndexes:

                    re_arranged_models.append(self.models[idx])
                
                self.attentionModelIndexes = [x for x in range(len(re_arranged_models))]
                
                other_models = list(set(self.models)-set(re_arranged_models))
                
                for model in other_models:

                    re_arranged_models.append(model)
                
                self.models = re_arranged_models
            
            self.metric_details = {}

            for model in self.models:
                if "metrics" in self.JSONdata[0]["outputs"][model]:
                    self.metric_details[model] = list(self.JSONdata[0]['outputs'][model]["metrics"].keys())
                    self.metric_details[model].append('None')
                else:
                    self.metric_details[model]=['None']
            
            self.sortedSecIndices = {model:{} for model in self.models}

            # st.text(self.sortedSecIndices)

            
            for model in self.metric_details:
                for metric in self.metric_details[model]:
                    if metric!='None':
                        self.sortedSecIndices[model][metric]= [i[0] for i in sorted(enumerate(self.JSONdata), key=lambda x:x[1]['outputs'][model]['metrics'][metric])]
                    else:
                        self.sortedSecIndices[model][metric] = [i for i in range(len(self.JSONdata))]

        else:

            # case where the user uploads data with only image path and posibly the corresponding ground truth.
            self.models = None
            self.sortedSecIndices = [i for i in range(self.len)]

        

    
    def parseOCRJson(self,dataPath):
        with open(dataPath,'r') as dataFile:
            data = json.load(dataFile)
        return data
    

    def getData(self,index):
        return self.JSONdata[index]
    

    def loadOCRData(self,dataPath):
        data = self.parseOCRJson(dataPath)
        for i in range(len(data)):
            if "outputs" in data[i]:
                for model in data[i]["outputs"]:
                    if "attentions" in data[i]["outputs"][model]:
                        data[i]["outputs"][model]["attentions"] = np.array(data[i]["outputs"][model]["attentions"]).reshape((-1,2))

        return data

    
    def loadImage(self,index):

        """
        on success : saves PIL image data object into the jsonData with corresponding index & returns numpy array of image 
        on failure : returns -1
        """

        if "image" in self.JSONdata[index]:
            try:
                im = ImageOps.grayscale(self.JSONdata[index]["image"])
                imageData = np.asarray(im, dtype=np.uint8)
                return imageData
            except:
                st.warning('Error in loading image array. ')
                return -1
        


        imagePath = self.JSONdata[index]["imagePath"]

        try:
            im = Image.open(imagePath)
        except:
            st.warning('The Image with path {imagePath} either does not exists or is not readable')
            return -1
            
        im = ImageOps.grayscale(im)
        img_data = np.asarray(im, dtype=np.uint8)

        self.JSONdata[index]["image"] = im

        return img_data
    
    def setCharLevelAtts(self,index,model):


        predicted_string = self.JSONdata[index]["outputs"][model]["prediction"]

        charLevelAtts = []
        start = 0
        end = 0
        atts = self.JSONdata[index]['outputs'][model]["attentions"]
        # try:

        for i in range(len(predicted_string)):
            loi = len(str(ord(predicted_string[i])))
            end = start+loi
            # print(end,atts.shape)
            if end >= atts.shape[0]:
                end = atts.shape[0]-1
            chStart = atts[start][0]
            chEnd = atts[end][1]

            charLevelAtts.append([chStart,chEnd])
            start = end
        
        self.JSONdata[index]["outputs"][model]["charLevelAtts"] = charLevelAtts
        
        # except:
        #     print('Some error in setting the CharLevelAttentions')
        
    
    def highlightImage(self,index,model,start,end,hcolor="#00FFFF",threshold=50):

        getRGB = lambda x : tuple(int(x[i:i+2], 16) for i in (0, 2, 4))

        rgbtuple = getRGB(hcolor.lstrip("#"))
        

        
        # accounting for backward mouse selection:
        if start > end:
            temp = start
            start = end
            end = start
        
        # load image if not already loaded:
        imageData = self.loadImage(index)
        
        if type(imageData) == int:
            return -1
        
        # return plain image on no selection
        if start==end :
            return imageData

        
        # if charLevelAttentions are not calculated, calculate them:

        try:
            atts = self.JSONdata[index]["outputs"][model]["charLevelAtts"]

        except:
            self.setCharLevelAtts(index,model)
            try:
                atts =  self.JSONdata[index]["outputs"][model]["charLevelAtts"]
            except:
                print('Some Issue with attentions')
                return -1

        
        # load your image_array:
        try:
            hImage = np.copy(imageData)
            hImage2 = np.copy(imageData)
            if len(hImage.shape)< 3:
                hImage = cv.cvtColor(hImage, cv.COLOR_GRAY2RGB)
                hImage2 = cv.cvtColor(hImage2, cv.COLOR_GRAY2RGB)

            try:
                b, g, r = cv.split(hImage)
                mask = (b > threshold) & (g > threshold) & (r > threshold)
                hImage[mask]= rgbtuple
                hImage2[:,atts[start][0]:atts[end][1],:] = hImage[:,atts[start][0]:atts[end][1],:]
            except IndexError:
                hImage[:,atts[start][0]:atts[len(self.JSONdata[index]["outputs"][model]["prediction"])-1][1],0] = rgbtuple

            return hImage2
        except:
            st.warning('An unwanted error has occured while trying to highlighted the subportion of the image.')
            return -1
    
    def getText(self,index,model,start,end):

    
        # print(start,end)
        try:
            mapping = self.JSONdata[index]["outputs"][model]["charLevelAtts"]

        except:
            self.setCharLevelAtts(index,model)
            try:
                mapping =  self.JSONdata[index]["outputs"][model]["charLevelAtts"]
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