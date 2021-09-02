# # import essential libraries
import streamlit as st
import SessionState

# # import pre-defined layouts

# import boundaryNetApp
from layouts.boxSupervision import boxSupervision
from layouts.fullyAutomatic import fullyAutomatic
from layouts.OCR.src import OCR



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
from config import metaDataDir,docVisorRepo,save_dir


try:
    st.set_page_config(page_title='docVisor',layout="wide")
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
        "dtype":"data type -- possible options are 'normal' and 'latex' -- mandatory only if latex", 
        "dataPaths": {
            "train": "/train/train_data.json",
            "val": "/val/val_data.json",
            "test": "/test/test_data.json"
        }
    }
}


pageLayoutFileMap = {

    "Box-supervised Region Parsing":boxSupervision,
    "Fully Automatic Region Parsing":fullyAutomatic,
    "OCR":OCR

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

    # """
    # # structure of metaData
    # {
    #     "{pageLayout}":{
    #         "pageName":mdata
    #     }
    # }

    # """
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
            if 'dtype' not in data["metaData"]:
                data["metaData"]['dtype'] = 'normal'

            if data["metaData"]["pageLayout"] not in list(pageLayoutFileMap.keys()):
                st.warning(f'Page Layout has to be one of '+" ".join(list(pageLayoutFileMap.keys())))
                return -1


            playout = data["metaData"]["pageLayout"]
            pname = data["metaData"]["pageName"]

            if playout not in metadata:
                metadata[playout] = {}


            try:
                if pname in metadata[playout]:
                    raise Exception
                metadata[playout][pname] = data
            except:
                st.warning('Value for key `pageName` has to be unique for each layout')
                return -1



    return metadata


def defineAppPageLayout(allMdatas):
    pages = {}
    # print(allMdatas)
    for page in allMdatas:
        pages[page]=pageLayoutFileMap[allMdatas[page]["metaData"]["pageLayout"]]

    return pages

def defineAppPageLayout2(allMdatas):

    pages = {}

    for playout in allMdatas:
        pages[playout] = {}
        for pageName in allMdatas[playout]:
            pages[playout][pageName] = pageLayoutFileMap[allMdatas[playout][pageName]["metaData"]["pageLayout"]]
    return pages

def getDirName(pageDetails):
    print('Creating Directory for this session')
    now = datetime.now()
    dirPath = now.strftime("%d_%m_%Y")
    mdir = save_dir+'/'+dirPath
    if not os.path.exists(mdir):
        os.mkdir(mdir)

    ## date/ : loaded
    createdSessionDir = False
    counter = 0
    while not createdSessionDir:
        try:
            os.mkdir(mdir+f'/{counter}')
            createdSessionDir = True
        except:
            counter+=1
    currPath = mdir+"/"+str(counter)+'/'

    for pageLayout in pageDetails:
        if not os.path.exists(currPath+pageLayout):
            os.mkdir(currPath+pageLayout)
        for pageName in pageDetails[pageLayout]:
            os.mkdir(currPath+pageLayout+'/'+pageName)
            

    return currPath

state = SessionState._get_state()


# create save directory for save operation:


# state.saveDirCreated = True

if state.isMetaDataLoaded is None:
    metaDataObjs = getLayoutMetaData()

    if metaDataObjs==-1:
        pass
    elif len(metaDataObjs)!=0 and type(metaDataObjs)==dict:
        state.isMetaDataLoaded = True
        state.metaDataObjs = metaDataObjs

if state.isMetaDataLoaded is True:
    pages = defineAppPageLayout2(state.metaDataObjs)

    if state.saveDirCreated is None or state.saveDirCreated is False:
        savePathPrefix = getDirName(pages)
        if type(savePathPrefix)==str:
            state.saveDirCreated = True
        state.savePathPrefix =savePathPrefix

    

    sc1,_,sc2 = st.sidebar.beta_columns([3,0.1,3])

    sc1.image("tool/images/iiit-new.png",width=125)
    sc2.image("tool/images/cvit-logo.jpeg",width=100)
    
    
    st.sidebar.title('DocVisor')

    selection = st.sidebar.selectbox("Go to", list(pages.keys()))

    pageName = st.sidebar.selectbox("Choose Page:",list(pages[selection].keys()),index=0)

    page = pages[selection][pageName]
    getkey = lambda : str(uuid4()).replace('-', '')

    if state.keys is None:
        print("State.keys are empty")
        state.keys = {}
    if selection not in state.keys:
        state.keys[selection] = {}
    if pageName not in state.keys[selection]:
        print(f'Yes {pageName} is getting initialized')
        state.keys[selection][pageName] = getkey()
    key = state.keys[selection][pageName]
    state.metaDataObjs[selection][pageName]["metaData"]["key"] = key
    state.metaDataObjs[selection][pageName]["metaData"]["savePath"] = state.savePathPrefix+selection+'/'+pageName
    page.app(metaData=state.metaDataObjs[selection][pageName])
