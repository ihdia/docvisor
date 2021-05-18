import streamlit as st
import SessionState
import streamlit.components.v1 as components
from ocrHelper import OCRHelper
import numpy as np
import random
import cv2
import base64
from PIL import Image
import io
from diffHelper import annotated_text, annotation
import difflib


_RELEASE = True

if not _RELEASE:
    _roi_selector = components.declare_component(
        "roi_selector",
        url="http://localhost:3001",
    )
    _text_highlighter = components.declare_component(
        "roi_selector",
        url="http://localhost:3002",
    )
else:
    # parent_dir = os.path.dirname(os.path.abspath(__file__))
    # build_dir = os.path.join(parent_dir, "frontend/build")
    _roi_selector = components.declare_component("roi_selector",

                                                 path="/home/user/hdia/hindola/hindola/visualizer/icdar-visualizer/streamlit/roi_selector/frontend/build")
    _text_highlighter = components.declare_component("text_highlighter",
                                                     path=r"/home/user/hdia/hindola/hindola/visualizer/icdar-visualizer/streamlit/text_highlighter/frontend/build")



def np_to_b64(img_data):
    img_data = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.jpg', img_data)
    pic_str = base64.b64encode(buffer).decode("utf-8")
    
    img_b64 = "data:image/jpeg;base64, " + pic_str
    imgdata = base64.b64decode(pic_str)
    im = Image.open(io.BytesIO(imgdata))
    # st.text(im.size)
    # st.image(img_b64)
    return img_b64


def roi_selector(img_b64, pred, ground, isEnabled,height, key,default={"start_px":-1,"end_px":-1}):
    default = {"start_px":-1,"end_px":-1,"key":key}
    component_value = _roi_selector(img_b64=img_b64, text=pred, isEnabled=isEnabled, default=default,key=key)
    return component_value


def text_highlighter(text, ranges, isEnabled,key, default = {"start_idx":-1,"end_idx":-1},font_size=20):
    component_value = _text_highlighter(text=text, ranges=ranges, isEnabled=isEnabled,font_size=font_size, default=default)
    return component_value


def get_ranges_to_highlight_text(startpx, endpx):
    if startpx == endpx:
        return []
    else:
        # print(startpx, endpx)
        return [{'start': random.randint(1, 10), 'end': random.randint(18, 25)}]

def getDiff(seqm):
    
    output = {}
    
    # i0 , i1 : for prediction

    # j0 , j1 : for groundTruth

    # note that this mapping works because for same set of indices we will not perform add/insert/delete

    for opcode, i0, i1, j0, j1 in seqm.get_opcodes():
        try:
            output[tuple([i0,i1,j0,j1])]=opcode
        except:
            raise RuntimeError("unexpected opcode while computing diffs.")
            
    return output

def visualizeDiff(ground,predicted,imageData,key,displayImage=False,font_size=30):

    # note the order is important:
    # we want to find how to convert predicted to ground
    # not the other way around

    if type(imageData)==np.ndarray:
        if displayImage:
            st.image(imageData)

    
    else:
        st.warning('Error in Loading Image -- Check your Command Line Terminal for more details')
        

    colors = {
        "equal":{
            "ground":"lightgreen",
            "predicted":"lightgreen"
        },
        "insert":{
            "ground":"#8C44DB", # light-purple
        },
        "delete":{
            "predicted":"#B5651D" # light-brown
            },

        "replace":{
            "ground":"lightblue",
            "predicted":"orange"
        }
    }
    sm = difflib.SequenceMatcher(None, predicted, ground)

    diffs = getDiff(sm)

    commonComponentIndex = 0

    predTextArgs = []
    groundTextArgs = []
    count = 1
    for info in diffs:
        i0,i1,j0,j1 = info
        opcode = diffs[info]

        if opcode in ["replace","equal"]:

            colorg = colors[opcode]["ground"]
            colorp = colors[opcode]["predicted"]

            predTextArgs.append((predicted[i0:i1],f"{count}",colorp))
            groundTextArgs.append((ground[j0:j1],f"{count}",colorg))
        
        if opcode == "insert":
            colorg = colors[opcode]["ground"]
            groundTextArgs.append((ground[j0:j1],f"{count}",colorg))
            
        
        
        if opcode == "delete":
            colorp = colors[opcode]["predicted"]
            predTextArgs.append((predicted[i0:i1],f"{count}",colorp))
        
        


        count+=1
    


    st.text("Ground:")
    annotated_text(
        *groundTextArgs,
        font_size=font_size
    )

    st.text("Predicted:")

    annotated_text(
        *predTextArgs,
        font_size=font_size
    )

    # loadNotation = st.checkbox('Display diff color coding',key='ocr')

    with st.beta_expander("diff color-coding notation"):
        st.markdown("""The above visualization, depicts the minimal operations
            required to convert the predicted string to the ground truth. Notice that every 
            distinct color bounded-text is also annotated with numbers. Also notice that for a
            color bounded component in the ground truth with annotation $i$, there could be a corresponding
            color bounded text annotated with the same number $i$ (the color of these two color-bounded texts need not be the same).
        """)
        st.markdown(
            """
            |Color of GT Component $i$ |Color of Predicted Component $i$|What does it Mean?|
            |---|---|----|
            |light-green|light-green|Component $i$ of GT and component $i$ of the Prediction are **Equal**|
            |light-purple|non-existent|**Insert** Component $i$ of GT after component $i-1$ of Prediction|
            |non-existent|light-brown|**Delete** Component $i$ of Prediction|
            |light-blue|orange|**Replace** component $i$ of Prediction with component $i$ of GT|
            """
        )


def displayMetrics(ocr,index):

    no_of_metrics = len(ocr.metrics)

    metricStrings = []

    for  metric in ocr.metrics:
        if metric !="None":
            mstring = f'**{metric} :** {ocr.JSONdata[index]["metrics"][metric]:.2f}'
            metricStrings.append(mstring)
    
    st.markdown(' , '.join(metricStrings))


##################################################
##################################################

"""
Definition of APP Layout:
"""

##################################################
##################################################



def app(key,metaData=None):
    

    # page layout data loader
    # data loads once -- gets cached.
    # if user wants to keep the app dynamic to changes in json file
    # comment out the @st.cache call above the initOCRHelper() function

    @st.cache(allow_output_mutation=True,suppress_st_warning=True)
    def initOCRHelper():

        """
        Input agrs: None

        output : Dictionary with OCRHelper objects initalized for each
                 dataclass defined in the jsonData file.

                Check ocrHelper file in the same directory for more details
        """

        print(f"Loading Data for {metaData['metaData']['pageName']}")

        subOCRs = {}

        for datasetClass in metaData["metaData"]["dataPaths"]: 
            jsonFile = metaData["metaData"]["dataPaths"][datasetClass]
            ocr = OCRHelper(jsonFile)
            subOCRs[datasetClass] = ocr
        return subOCRs
    

    

    ocrObjects = initOCRHelper()

    if ocrObjects!=-1:
        dataTypes = list(ocrObjects.keys())


        # set session state. Important for two way communication.
        state = SessionState._get_state()

        ## Page Heading:
        _, col2, _ = st.beta_columns([1, 1, 1])

        with col2:
            st.title("OCR Attention Visualizer")
        
        # add a bookmarks variable:

        if state.bookmarks is None:

            state.bookmarks = {
                key:[]
            }
        
        elif key not in state.bookmarks:
            state.bookmarks[key] = [] # [{"train":index}]
        

        if len(state.bookmarks[key])!=0:
            dataTypes.append("bookmarks")
        # Side bar dataset Selection

        dataClass = st.sidebar.selectbox(
            "Choose the Dataset Class",
            dataTypes,
            index=0
        )


        if dataClass!="bookmarks":
            ocr = ocrObjects[dataClass]
        
            sort_by = st.sidebar.selectbox(
                "Sort By",
                ocr.metrics,
                index=0
            )

            if sort_by!='None':
                order = st.sidebar.selectbox(
                "Order",
                ["ascending", "descending"],
                index=0
            )

            else:
                order = 'ascending'



        

        beginnerSelectData = {
                "start":-1,
                "end":-1
            }
        
        if state.pageDetails is None:

            state.pageDetails = {
                key:{
                    dataClass:{
                        "ascending":{x:0 for x in ocr.metrics},
                        "descending":{x:0 for x in ocr.metrics}
                    }
                }
            }
        
        if key not in state.pageDetails:
            state.pageDetails[key] = {
                dataClass:{
                        "ascending":{x:0 for x in ocr.metrics},
                        "descending":{x:0 for x in ocr.metrics}
                }
            }

        if dataClass not in state.pageDetails[key]:
            if dataClass!="bookmarks":
                state.pageDetails[key][dataClass] = {
                        "ascending":{x:0 for x in ocr.metrics},
                        "descending":{x:0 for x in ocr.metrics}
                }
        
            else:
                state.pageDetails[key][dataClass] = 0


        if dataClass!="bookmarks":

            if order == 'ascending':

                index = ocr.sortedSecIndices[sort_by][state.pageDetails[key][dataClass][order][sort_by]]

            else:

                index = ocr.sortedSecIndices[sort_by][ocr.len-1-state.pageDetails[key][dataClass][order][sort_by]]
        
        else:

            index = list(state.bookmarks[key][state.pageDetails[key][dataClass]].values())[0]

            ocr = ocrObjects[list(state.bookmarks[key][state.pageDetails[key][dataClass]].keys())[0]]


        if state.selection_data is None:

            state.selection_data = {
                key:beginnerSelectData
            }
        # st.json(beginnerSelectData)

        if key not in state.selection_data:
            state.selection_data[key] = beginnerSelectData


        start = state.selection_data[key]['start']
        end = state.selection_data[key]['end']

        # prev1, _ ,next1 = st.beta_columns([1, 10, 1])

        with st.beta_expander("Visualizer Settings"):
            activeComponent = st.radio(
                "Activate Component",
                ["Text Selection","Image Selection"],
                index = 0
            )

        if state.textRange is None:
                state.textRange = {
                    key:{
                        "start_idx":-1,
                        "end_idx":-1
                    }
                }

            
        elif key not in state.textRange:

            # print('initializing')

            state.textRange = None

            state.textRange = {
                    key:{
                        "start_idx":-1,
                        "end_idx":-1
                    }
                }


        if state.crop_range is None:
                state.crop_range = {
                    key:{
                        "start_px":-1,
                        "end_px":-1
                    }
                }
        elif key not in state.crop_range:
            # state.crop_range = None
            state.crop_range[key] = {
                        "start_px":-1,
                        "end_px":-1
                }
        
        st.sidebar.markdown("## Settings:")

        if state.fontSize is None:
            state.fontSize = {
                "playground":30,
                "diffViz":20
            }
        if state.commonFontSize is None:
            state.commonFontSize = False

        if state.highlightColor is None:
            state.highlightColor = "#00FFFF"
        # Font Size Input
        with st.sidebar.beta_expander("Play Ground:"):
            st.markdown("### Text Font Size:")
            state.fontSize["playground"] = st.slider("Choose Font Size(px) for the text playground via slide bar" , 10,300,state.fontSize["playground"])

            pgfontInput = st.text_input("Or enter a font value",state.fontSize["playground"],key="playground")
            if pgfontInput!='':
                try:
                    state.fontSize["playground"] = int(pgfontInput)
                except:
                    st.warning("Kindly input a valid font size : non-negative integer")
            
            st.markdown("---------")
            st.markdown("highlighted image color")
            state.highlightColor = st.color_picker("Choose a color",value=state.highlightColor) 
        
        with st.sidebar.beta_expander("diff Visualizer:"):
            st.markdown("### Diff Visualizer Font Size:")

            if st.checkbox("Set Font Size same as that of text-playground?",value=state.commonFontSize):
                state.commonFontSize = True
                state.fontSize["diffViz"] = state.fontSize["playground"]
            else:
                state.fontSize["diffViz"] = st.slider("Choose Font Size(px) for the diff visualizer via slide bar" , 10,300,state.fontSize["diffViz"])
                diffVizfontInput = st.text_input("Or enter a font value",state.fontSize["diffViz"],key="diffViz")
                if diffVizfontInput!='':
                    try:
                        state.fontSize["diffViz"] = int(diffVizfontInput)
                    except:
                        st.warning("Kindly input a valid font size : non-negative integer")
            
            st.markdown("Image Settings:")
            
            if state.displayImageDiff is None:
                state.displayImageDiff = False

            state.displayImageDiff = st.checkbox('Display Image in Diff View Area?')
            
            


        
        ## Loading Features.

        # IMAGE SELECTION COMPONENT
        
        if activeComponent == 'Image Selection':
            img_data = ocr.highlightImage(index, -1, -1,ocr.JSONdata)
            # st.warning('Error in Loading Image -- Check your Command Line Terminal for more details')

            #             else:

            if type(img_data)==np.ndarray:
                
                if dataClass=="bookmark":

                    st.markdown("# 🔖 Image:")
                
                else:

                    st.markdown("# Image")
                st.markdown('-----------------')

                # Load annotation ground truth and prediction
                ground = ocr.JSONdata[index]["annotation"]["groundTruth"]
                predicted = ocr.JSONdata[index]["annotation"]["prediction"]

                # get image portion to be cropperd
                # the react component is coded such that 
                # the image re-size in the web browser will not effect the getText function
                # scaling is taken care off by the react component.
                crop_range = roi_selector(

                                        img_b64=np_to_b64(img_data),
                                        pred=predicted,
                                        ground=ground, 
                                        isEnabled=True,
                                        height=img_data.shape[0],
                                        default={"start_px":-1,"end_px":-1},
                                        key=key
                                )
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


                ranges = ocr.getText(index,start_px, end_px,ocr.JSONdata)

                # Text Display: Page Layout
                st.markdown('-----------------')
                st.markdown('### Predicted Text:')


                # highlight the corresponding text
                # does not give any return value of use when we on Image Selection Component.
                # will highlight corresponding portion of image with yello background.

                text_highlighter(
                                text=predicted, 
                                ranges=ranges, 
                                isEnabled=False,
                                key=key,
                                font_size=state.fontSize["playground"]
                            )


                st.markdown('### Ground Truth:')
                styleString = "<style>.big-font {font-size:"+str(state.fontSize["playground"])+"px; !important;}</style>"
                st.markdown(styleString, unsafe_allow_html=True)
                st.markdown(f'<p class="big-font">{ground}</p>', unsafe_allow_html=True)
                st.markdown('-----------------')


                st.markdown('#### Metrics (in fractions):')
                displayMetrics(ocr,index)
            
            else:
                # handle error of image not being a proper data-type
                st.warning('Error in Loading Image -- Check your Command Line Terminal for more details')
        
        elif activeComponent == "Text Selection":

            # Text Selection Component : Select a portion of the text
            # Corresponding Image portion will be highlighted using 
            # attention matrix. 


            # Note that ranges is empty here since we are not going to 
            # highlight the text. Rather we will be highlighting the image.

            ranges = []

            # initialize ground and prediction data
            ground = ocr.JSONdata[index]["annotation"]["groundTruth"]
            predicted = ocr.JSONdata[index]["annotation"]["prediction"]

            # load image. 
            # "start_idx" and "end_idx" correspond to the start index and end index
            # of the selected text of the prediction. Initially these values are set to
            # -1 meaning that dont highlight any portion of the image.

            # call the ocr.highlightImage function to get numpy array that is highlighted.

            img_data = ocr.highlightImage(
                                            index, 
                                            state.textRange[key]["start_idx"], 
                                            state.textRange[key]["end_idx"],
                                            ocr.JSONdata,
                                            hcolor=state.highlightColor
                                        )


            if type(img_data)==np.ndarray:

                if dataClass=="bookmark":
    
                    st.markdown("# 🔖 Image:")
                
                else:

                    st.markdown("# Image")

                st.markdown('-----------------')
                
                # Load the image : Image Selection disabled. 
                # roi_selector :react component.
                # Note : Do not pass on page key. Components do not get updated.

                roi_selector(
                                key=None,
                                img_b64=np_to_b64(img_data),
                                pred=predicted, 
                                isEnabled=False, 
                                ground=ground,
                                height=img_data.shape[0]
                            )
                



                st.markdown('-----------------')
                st.markdown('### Predicted Text:')
                    

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
                
                st.markdown('### Ground Truth:')
                styleString = "<style>.big-font {font-size:"+str(state.fontSize["playground"])+"px; !important;}</style>"
                st.markdown(styleString, unsafe_allow_html=True)    
                st.markdown(f'<p class="big-font">{ground}</p>', unsafe_allow_html=True)
                st.markdown('-----------------')


                st.markdown('#### Metrics (in fractions):')
                displayMetrics(ocr,index)
            else:
                # handle error of image not being a proper data-type
                st.warning('Error in Loading Image -- Check your Command Line Terminal for more details')
        
        

        if ocr.len > 1:
            if dataClass!="bookmarks":
                currentLoc = state.pageDetails[key][dataClass][order][sort_by]
                state.pageDetails[key][dataClass][order][sort_by] = st.slider(
                                                        "Select image Index",
                                                        0,
                                                        ocr.len-1,
                                                        state.pageDetails[key][dataClass][order][sort_by]
                                                    )
                if state.pageDetails[key][dataClass][order][sort_by]!=currentLoc:
                    state.selection_data = None
                    state.textRange = None
                    state.crop_range = None


                prev, _ ,next = st.beta_columns([1, 10, 1])
                
                
                if next.button("Next",key=key):

                    if state.pageDetails[key][dataClass][order][sort_by] + 1 >= ocr.len:
                        st.warning('This is the last image.')
                    else:
                        state.pageDetails[key][dataClass][order][sort_by] += 1

                        # re-initialize all your data
                        # :)


                        state.selection_data = None
                        state.textRange = None
                        state.crop_range = None

                if prev.button("Previous",key=key):

                    if state.pageDetails[key][dataClass][order][sort_by] - 1 < 0:

                        st.warning('This is the First image. Cannot go backwards')

                    else:
                        state.pageDetails[key][dataClass][order][sort_by] -= 1
                        state.selection_data = None
                        state.textRange = None
                        state.crop_range = None

                inpIndex = st.text_input(f'Input an index value between 0 and {ocr.len-1}',state.pageDetails[key][dataClass][order][sort_by])
                if inpIndex=='':
                    pass
                else:
                    try:
                        inpIndex = int(inpIndex)
                        
                        if inpIndex < 0 or inpIndex > ocr.len-1:
                            raise Exception

                        # update the state variable so that it reflects on the slider as well.
                        state.pageDetails[key][dataClass][order][sort_by] = inpIndex
                    except:
                        st.warning(f"Please input a integer value from 0 to {ocr.len-1}")
            
            else:
                if len(state.bookmarks[key])>1:
                    currentLoc = state.pageDetails[key][dataClass]
                    state.pageDetails[key][dataClass] = st.slider(
                                                        "Select image Index",
                                                        0,
                                                        len(state.bookmarks[key])-1,
                                                        state.pageDetails[key][dataClass]
                                                    )
                    if state.pageDetails[key][dataClass]!=currentLoc:
                        state.selection_data = None
                        state.textRange = None
                        state.crop_range = None


                    prev, _ ,next = st.beta_columns([1, 10, 1])
                    
                    
                    if next.button("Next",key=key):

                        if state.pageDetails[key][dataClass] + 1 >= len(state.bookmarks[key]):
                            st.warning('This is the last image.')
                        else:
                            state.pageDetails[key][dataClass] += 1

                            # re-initialize all your data
                            # :)


                            state.selection_data = None
                            state.textRange = None
                            state.crop_range = None

                    if prev.button("Previous",key=key):

                        if state.pageDetails[key][dataClass] - 1 < 0:

                            st.warning('This is the First image. Cannot go backwards')

                        else:
                            state.pageDetails[key][dataClass] -= 1
                            state.selection_data = None
                            state.textRange = None
                            state.crop_range = None

                    inpIndex = st.text_input(f'Input an index value between 0 and {len(state.bookmarks[key])-1}',state.pageDetails[key][dataClass])
                    if inpIndex=='':
                        pass
                    else:
                        try:
                            inpIndex = int(inpIndex)
                            
                            if inpIndex < 0 or inpIndex > ocr.len-1:
                                raise Exception

                            # update the state variable so that it reflects on the slider as well.
                            state.pageDetails[key][dataClass] = inpIndex
                        except:
                            st.warning(f"Please input a integer value from 0 to {len(state.bookmarks[key])-1}")
                else:

                    st.warning("Note: There is only one image in your bookmarks for this layout.")
        
        

        st.markdown('## Other Visualizations')
        st.markdown('### Visualize diffs')



        visualizeDiff(ground,predicted,img_data,key=key,displayImage=state.displayImageDiff,font_size=state.fontSize["diffViz"])

        with st.beta_expander("Attention GIF"):
            
            agree = st.checkbox('Load Attention GIF',key=key)

            if agree:
                file_ = open(ocr.JSONdata[index]["gifPATH"], "rb")
                contents = file_.read()
                data_url = base64.b64encode(contents).decode("utf-8")
                file_.close()

                res = st.markdown(
                    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
                    unsafe_allow_html=True,
                )
        # st.json(state.bookmarks)
        if dataClass!='bookmarks':
            if st.button("Bookmark 🔖"):
                bookMarkData = {dataClass:index}
                if bookMarkData in state.bookmarks[key]:
                    st.warning("Page already bookmarked")
                else:
                    state.bookmarks[key].append({dataClass:index})
                    st.success("Successfully bookmarked")
        
        if state.toSaveImages is None:
            state.toSaveImages = {
                key:[]
            }

        elif key not in state.toSaveImages:

            state.toSaveImages[key] = []

        if st.button("Save 💾"):
            st.markdown("NOT YET IMPLEMENTED!")


        state.prevKey = key
        state.sync()