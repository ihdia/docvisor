import streamlit as st
import numpy as np
import io
from layouts.OCR.src.helpers import *
from layouts.OCR.src.frontendbuilds import *
from layouts.OCR.src.metrics import *
from layouts.OCR.src.headingDisplay import *


def loadInteractiveTextComponent(key,index,dataClass,model,ocr,state,textSelectorOn,font_size):

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

    # load the predicted text
    # state.sync()

    try:
        predicted = ocr.JSONdata[index]['outputs'][model]["prediction"]
    except:
        predicted = None

    if textSelectorOn == True:

        # also equivalent to roiSelector is OFF.

        # Text Selection Component : Select a portion of the text
        # Corresponding Image portion will be highlighted using
        # attention matrix.


        # Note that ranges is empty here since we are not going to
        # highlight the text. Rather we will be highlighting the image.


        ranges = []

        # ensure that predicted string is not None

        if predicted is not None and type(predicted)==str:

            # load model heading with formatted style

            displayModelHeading(model,'attention-model')

            try:
                prevTextRange = state.textRange[key]
            except KeyError:
                prevTextRange = None
            fsize = state.fontSize["playground"]
            selectedTextRange  = text_highlighter(
                                                        key = key+model+dataClass+str(index)+str(fsize),
                                                        text = predicted,
                                                        ranges = [], 
                                                        isEnabled=True,
                                                        default = {"start_idx":-1,"end_idx":-1},
                                                        font_size=state.fontSize["playground"]
                                                    )
            # print(selectedTextRange)
            if selectedTextRange!=state.textRange[key][model]:

                state.textRange[key][model] = selectedTextRange


                state.textRangeModel = model
                

            if key != state.prevKey:
                state.textRange = {
                        key:{

                            model:{
                                    "start_idx":-1,
                                    "end_idx":-1
                            }
                        }
                }

            selectedTextRange = None

        else:

            st.warning(f'Prediction output of model {model} is either not there in the data or is of invalid form.')
    
    elif textSelectorOn == False:

        # equivalent to ImageSelection is On;

        try:

            start_px = state.crop_range[key]["start_px"]
            end_px = state.crop_range[key]["end_px"]

        except KeyError:

            start_px = -1
            end_px = -1

        # use the getText function to get the range of text that needs
        # to be highlighted. Checkout the ocrHelper module for more
        # clarity


        ranges = ocr.getText(index,model,start_px, end_px)


        # Text Display: Page Layout

        if predicted is not None:

            # st.markdown(f'## {model}*')
            displayModelHeading(model,'attention-model')


            # highlight the corresponding text
            # does not give any return value of use when we on Image Selection Component.
            # will highlight corresponding portion of image with yellow background.
            text_highlighter(
                            key=None,
                            text=predicted,
                            ranges=ranges,
                            isEnabled=False,
                            font_size=state.fontSize["playground"]
                        )

