# # import essential libraries
import streamlit as st
import SessionState

# # import pre-defined layouts

import boundaryNetApp
import fullyAutomaticApp
import OCRapp



# # other python libraries
import re
import os
import sys
import pathlib
import json
import fnmatch
from datetime import datetime
from uuid import uuid4



# # import config file
from config import metaDataDir,docVisorRepo


try:
    st.set_page_config(layout="wide")
except:
    pass



jsonDataFormat = {
    "metaData": {
        "pageLayout": "str: one of 'OCR', 'Region','FullDocument'",
        "pageName": "string : Any Name of your interest",
        "dataPaths": {
            "classification1": "path/to/classification1/json/metadata",
            "classification2": "path/to/classification2/json/metadata",
            "classification3": "path/to/classification3/json/metadata"
        }
    }
}

jsonDataExample = {
    "metaData": {
        "pageLayout": "OCR",
        "pageName": "Sanskrit-OCR",
        "dataPaths": {
            "train": "/train/train_data.json",
            "val": "/val/val_data.json",
            "test": "/test/test_data.json"
        }
    }
}


pageLayoutFileMap = {

    "Region":boundaryNetApp,
    "FullDocument":fullyAutomaticApp,
    "OCR":OCRapp

}


def displayMissingKeyErrorMessage(missingKey,jsonFile):
    st.error(f"""Error Loading Page : key `{missingKey}` missing in file {metaDataDir+"/"+jsonFile}.
    Kindly visit the {docVisorRepo} to know more about the layout format.             
    """)
    st.text('The general metadata file format is as follows:')
    st.json(jsonDataFormat)
    st.text("Following is an example of JSON format for the OCR layout")
    st.json(jsonDataExample)
    st.warning('kindly update/remove the corresponding file and then refresh this page')

def displayInvalidTypeJSONError(invalidKey,jsonFile):

    st.error(f"""Error Loading Page : value of key `{invalidKey}` in file is {metaDataDir+"/"+jsonFile} of invalid datatype.
    Kindly visit the {docVisorRepo} to know more about the layout format.
                
    """)
    st.text('The general metadata file format is as follows:')
    st.json(jsonDataFormat)
    st.text("Following is an example of JSON format for the OCR layout")
    st.json(jsonDataExample)
    
    st.warning('kindly update/remove the corresponding file and then refresh this page')
    


def getLayoutMetaData():
    metadata = {}
    for file in os.listdir(metaDataDir):
        if fnmatch.fnmatch(file, '*.json'):
            with open(metaDataDir+'/'+file) as f:
                data = json.load(f)


            if "metaData" not in data:
                displayMissingKeyErrorMessage(missingKey="metaData",jsonFile=file)
                return -1
            
            if type(data["metaData"])!=dict:
                displayInvalidTypeJSONError("metaData",file)
                return -1

            for key in ["pageLayout","pageName","dataPaths"]:
                if key not in data["metaData"]:
                    displayMissingKeyErrorMessage(missingKey="metaData",jsonFile=file)
                    return -1
                if key!='dataPaths' and type(data["metaData"][key])!=str:
                    displayInvalidTypeJSONError(key,file)
                    return -1
                elif key == 'dataPaths' and type(data["metaData"][key])!=dict:
                    displayInvalidTypeJSONError(key,file)
                    return -1


            if data["metaData"]["pageLayout"] not in list(pageLayoutFileMap.keys()):
                st.warning(f'Page Layout has to be one of '+" ".join(list(pageLayoutFileMap.keys())))
                return -1

            
            try:
                if data["metaData"]["pageName"] in metadata:
                    raise Exception
                metadata[data["metaData"]["pageName"]] = data
            except:
                st.warning('Value for key `pageName` has to be unique for each layout')
                return -1

            # print(metadata)


    return metadata


def defineAppPageLayout(allMdatas):
    pages = {}
    # print(allMdatas)
    for page in allMdatas:
        pages[page]=pageLayoutFileMap[allMdatas[page]["metaData"]["pageLayout"]]

    return pages

def getDirName():
    print('Creating Directory for this session')
    now = datetime.now()
    dirPath = now.strftime("%d_%m_%Y/%H_%M_%S") 
    # dt_time = now.strftime("%H_%M_%S")
    print(dirPath)
    return dirPath

state = SessionState._get_state()

if state.isMetaDataLoaded is None:
    metaDataObjs = getLayoutMetaData()

    if metaDataObjs==-1:
        pass
    elif len(metaDataObjs)!=0 and type(metaDataObjs)==dict:
        state.isMetaDataLoaded = True
        state.metaDataObjs = metaDataObjs

if state.isMetaDataLoaded is True:
    # st.balloons()
    # st.balloons()
    # st.balloons()
    # st.success('The Metadata has been successfully loaded.')


    pages = defineAppPageLayout(state.metaDataObjs)

    # if state.dirInfo is None:
    #     state.dirInfo = getDirName()

    #     for key in pages:
    #         res = re.split(',|_|-|!| ', key)
    #         subDir = ''.join(res)
    #         os.makedirs(state.dirInfo+'/'+subDir, exist_ok=True)
    #         print("Dir",state.dirInfo+'/'+subDir)
            

    


    
    st.sidebar.title('DocVisor')
    # st.sidebar.write(pages)
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    st.text(selection)
    getkey = lambda : str(uuid4()).replace('-', '')
    if state.keys is None:
        state.keys = {selection: getkey()}
    elif selection not in state.keys:
        state.keys[selection] = getkey()
    key = state.keys[selection]

    page.app(key=key,metaData=state.metaDataObjs[selection])


