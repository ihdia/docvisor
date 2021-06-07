import streamlit as st
import numpy as np
import io
from layouts.OCR.src.helpers import *
from layouts.OCR.src.frontendbuilds import *
from layouts.OCR.src.metrics import *
from uuid import uuid4

"""
This file contains code to load the interactive image component.
The necessary condition for an interactive roi_selector component
to be loaded is that there should be atleast one model with attentions 
in the data provided by the user. 
"""


def loadInteractiveImageComponent(key,index,dataClass,model,ocr,state,roiSelectorOn,primaryModel):

    """
    key : is the layout page -- key. This is meant to take care of
          multiple instances of the same type of layout page. The user need 
          not generate this on his own. docvisor.py does it at load every
          instance of a layout.

    dataClass : The classification the user has made for his various dataclasses
                provided as meta data to the docvisor -- OCR layout. For example
                train, test, and validation is one very common classification

    model: the ocr layout tool allows the user to compare multiple models. We need
            this variable for proper navigation and data retrieval of predicted text/
            attention details.

    
    """

    if roiSelectorOn == True:

        # for the first time load an image without any highlight.
        # since roi_selector is on, we are really not highlighting
        # anything on the image.

        # get an image that does not highlight any sub-portion of it.
        img_data = ocr.highlightImage(index,model, -1, -1)


        # ensure that the data receieved from the OCRhelper function is actually valid
        if type(img_data)==np.ndarray:

            # cool feature where the user can see if he has already bookmarked/saved the image.
            extraChars = ''

            if dataClass!="bookmarks":

                if {dataClass:index} in state.bookmarks[key]:
                    extraChars += '🔖'

                if {dataClass:index} in state.savedData[key]:
                    extraChars+='💾'
            else:
                extraChars += '🔖'
                if state.bookmarks[key][state.pageDetails[key][dataClass]] in state.savedData[key]:
                    extraChars+='💾'
            
            st.markdown(f"## {extraChars} Image")
            st.markdown('-----------------')

            crop_range = roi_selector(

                                img_b64=np_to_b64(img_data),
                                isEnabled=True,
                                height=img_data.shape[0],
                                default={"start_px":-1,"end_px":-1},
                                key=key
                        )
        
            # st.info("This image is taken from the collection: "+generateInfo())
            # output of roi_slector : {"<page-key>":{"start_px":-1,"end_px":-1}}

            toUpdateKey = crop_range["key"]


            # update the state of the key corresponding to the component
            # note that since streamlit works in a particular fashion,
            # the keys need not match. Hence In order to take care of
            # inconsistent update, we pass on keys to the components
            # so that it is taken care of.


            state.crop_range[toUpdateKey] = {

                "start_px":crop_range["start_px"],
                "end_px":crop_range["end_px"]

            }

            # if the present instance of layout is different from the updated key
            # initialize its datastructure. Do not propagate changes of previous page
            # onto the current page.


            if key!=toUpdateKey:

                state.crop_range[key] = {
                    "start_px":-1,
                    "end_px":-1
            }
    
    else:

        # this would imply that the text selection component 
        # is on. Therefore use the the text_selection components
        # updated state variables and load the corresponding
        # highlighted sub-portion of the image.

        # state.textRange variable should carry all information
        # of the text substring selected.

        

        if (key==state.prevKey and (dataClass!=state.prevDataClass or (dataClass!='bookmarks' and primaryModel!=state.prevPrimaryModel))):
            # print('Reset')
            state.textRange = {
                    key:{
                            model:{
                                "start_idx":-1,
                                "end_idx":-1
                            }
                    }
            }
            start = -1
            end = -1
        else:

            if state.textRangeModel is None:
                start = state.textRange[key][model]["start_idx"]
                end = state.textRange[key][model]["end_idx"]
            else:
                try:
                    # print(state.textRangeModel)
                    start = state.textRange[key][state.textRangeModel]["start_idx"]
                    end = state.textRange[key][state.textRangeModel]["end_idx"]
                except :
                    start = -1
                    end = -1

        
        # st.text(state.textRange)

        # print(start,end)
        img_data = ocr.highlightImage(
                                index,
                                model,
                                start,
                                end,
                                hcolor=state.highlightColor,
                                threshold=state.threshold[key]
                            )

        # check for image validity:
        if type(img_data)==np.ndarray:
            
            extraChars = ''
            if dataClass!="bookmarks":
                if {dataClass:index} in state.bookmarks[key]:
                    extraChars += '🔖'
                if {dataClass:index} in state.savedData[key]:
                    extraChars+='💾'
            else:
                extraChars += '🔖'
                if state.bookmarks[key][state.pageDetails[key][dataClass]] in state.savedData[key]:
                    extraChars+='💾'
            st.markdown(f"## {extraChars} Image")

            st.markdown('-----------------')

            # Load the image : Image Selection disabled.
            # roi_selector :react component.
            # Note : Do not pass on page key. Components do not get updated.
            # if "attentions" in ocr.JSONdata[index]:
            roi_selector(
                            key=str(uuid4()),
                            img_b64=np_to_b64(img_data),
                            isEnabled=False,
                            height=img_data.shape[0]
                        )