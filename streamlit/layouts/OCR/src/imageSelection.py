
import streamlit as st
import numpy as np
import io
from layouts.OCR.src.helpers import *
from layouts.OCR.src.frontendbuilds import *
from layouts.OCR.src.metrics import *


def displayImageSelectionComponent(key,index,dataClass,model,ocr,state,mno):


    """
    This function assumes that the data has an attentions field.
    """

    # load Image
    img_data = ocr.highlightImage(index,model, -1, -1)

    # ensure that the data receieved from the OCR API is actually valid
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

        # Load annotation ground truth and prediction
        
        try:
            predicted = ocr.JSONdata[index]['outputs'][model]["prediction"]
        except:
            predicted = None

        # get image portion to be cropperd
        # the react component is coded such that
        # the image re-size in the web browser will not effect the getText function
        # scaling is taken care off by the react component.

        crop_range = roi_selector(

                                img_b64=np_to_b64(img_data),
                                pred=predicted,
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

        # Handling errors of possible updates that could have missed
        # if key is present, load it (since we have loaded properly)
        # else re-initialize the data and load -1,-1 which is default.

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
            style_def =  "<style>.model-heading {background-color: orange;display: inline-block;text-align:center;padding: 0.5em 0.2em 0.8em 0.5em;!important;}</style>"
            st.markdown(style_def, unsafe_allow_html=True)
            st.markdown(f'## <p class="model-heading"> {model} : </p>',unsafe_allow_html=True)
            # st.markdown('-----------------')
            # st.markdown('### Predicted Text:')


            # highlight the corresponding text
            # does not give any return value of use when we on Image Selection Component.
            # will highlight corresponding portion of image with yellow background.
            
            # if "attentions" in ocr.JSONdata[index]:
            text_highlighter(
                            text=predicted,
                            ranges=ranges,
                            isEnabled=False,
                            key=key,
                            font_size=state.fontSize["playground"]
                        )

        if "metrics" in ocr.JSONdata[index]['outputs'][model]:
            st.markdown('#### Metrics (in fractions):')
            displayMetrics(ocr,index,model)
        
        # st.info("This image is taken from the collection: "+generateInfo())
        

    else:
        # handle error of image not being a proper data-type
        st.warning('Error in Loading Image -- Check your Command Line Terminal for more details')