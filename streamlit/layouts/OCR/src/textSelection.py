import streamlit as st
import numpy as np
import io
from layouts.OCR.src.helpers import *
from layouts.OCR.src.frontendbuilds import *
from layouts.OCR.src.metrics import *


def displayTextSelectionComponent(key,index,dataClass,model,ocr,state,mno):

    # Text Selection Component : Select a portion of the text
    # Corresponding Image portion will be highlighted using
    # attention matrix.


    # Note that ranges is empty here since we are not going to
    # highlight the text. Rather we will be highlighting the image.

    ranges = []

    # initialize prediction data
    try:
        predicted = ocr.JSONdata[index]['outputs'][model]["prediction"]
    except:
        predicted = None

    # load image.
    # "start_idx" and "end_idx" correspond to the start index and end index
    # of the selected text of the prediction. Initially these values are set to
    # -1 meaning that dont highlight any portion of the image.

    # call the ocr.highlightImage function to get numpy array that is highlighted.


    if key==state.prevKey and dataClass!=state.prevDataClass:
            state.textRange = {
                    key:{
                        "start_idx":-1,
                        "end_idx":-1
                    }
            }

    img_data = ocr.highlightImage(
                                    index,
                                    model,
                                    state.textRange[key]["start_idx"],
                                    state.textRange[key]["end_idx"],
                                    hcolor=state.highlightColor,
                                    threshold=state.threshold[key]
                                )


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
                        key=None,
                        img_b64=np_to_b64(img_data),
                        pred=predicted,
                        isEnabled=False,
                        height=img_data.shape[0]
                    )
        # else:


        #     st.warning('The data for this image does not have attention matrix provided.')
        #     st.image(img_data)


        if predicted is not None:
            st.markdown(f'## {model}*')
            # st.markdown('-----------------')
            # st.markdown('### Predicted Text:')

            # if "attentions" in ocr.JSONdata[index]:
            state.textRange[key] = text_highlighter(
                                                        key = key,
                                                        
                                                        text = predicted,
                                                        ranges = ranges, isEnabled=True,
                                                        default = {
                                                                    "start_idx":-1,
                                                                    "end_idx":-1
                                                                },
                                                        font_size = state.fontSize["playground"]
                                                )
                # handling multiple instances of same OCR page layout:
                # if present pagelayout key isnt same as the one that sent data
                # to the text_highlighter, then re-initalize the datastructre.

            if key != state.prevKey:
                state.textRange = {
                        key:{
                            "start_idx":-1,
                            "end_idx":-1
                        }
                }
        

        if 'metrics' in ocr.JSONdata[index]['outputs'][model]:
            st.markdown('#### Metrics (in fractions):')
            displayMetrics(ocr,index,model)
        
        # st.info("This image is taken from the collection: "+generateInfo())
    else:
        # handle error of image not being a proper data-type
        st.warning('Error in Loading Image -- Check your Command Line Terminal for more details')

