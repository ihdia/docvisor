import streamlit as st
import json
import SessionState
import os
import layouts.fullyAutomatic.PlotImage as PlotImage

@st.cache(allow_output_mutation=True)
def get_json_data(metaData):
    """
    Fetches the data associated with the current page layout selected from the metadata

    The function is cached to avoid redundant I/O operations every time page layout is rerun

    Parameters:
    metaData (dict): Contains the metadata associated with the current layout

    Returns:
    data (dict): Key-value pairs of data, with the keys being the datasets and the values being the associated data
    """

    data = {}

    for dataset in metaData["dataPaths"].keys():

        if "dataFormat" in metaData.keys():
            
            if not os.path.exists("/".join(metaData["dataPaths"][dataset].split("/")[:-1]) + "/" + metaData["dataPaths"][dataset].split("/")[-1].split(".")[0] + "-" + metaData["dataFormat"] + ".json"):
                os.system("python3 parse_"+metaData["dataFormat"]+"_instance"+".py "+metaData["dataPaths"][dataset])
        
            with open("/".join(metaData["dataPaths"][dataset].split("/")[:-1]) + "/" + metaData["dataPaths"][dataset].split("/")[-1].split(".")[0] + "-" + metaData["dataFormat"] + ".json","r") as f:
                loadedData = json.load(f)
        else:
            with open(metaData["dataPaths"][dataset],"r") as f:
                loadedData = json.load(f)
        
        data[dataset] = loadedData
    
    if "outputMasks" in metaData.keys():
        outputMasks = metaData["outputMasks"]
    else:
        outputMasks = None
    
    if "defaultDisplayed" in metaData.keys():
        defaultDisplayed = metaData["defaultDisplayed"]
    else:
        defaultDisplayed = None

    return data,outputMasks,defaultDisplayed

def filter_by_dataset(dataset,data):
    """
    Filters data by user-selected dataset, and returns the filtered data

    Parameters:
    dataset (string): Dataset selected by the user from the dropdown
    data (dict): Key-value pairs of data, with the keys being the datasets and the values being the associated data

    Returns:
    dataset_filtered_data (dict): Dict of data for a particular dataset, with keys being document ID and values being associated data
    """

    dataset_filtered_data = data[dataset]
    return dataset_filtered_data

def organize_regions(dataset,dataset_filtered_data):
    """
    Creates a dict with keys being region label and associated value being a list of data for that region label
    Since bookmarks can be made either regionwise or full document-wise, the data generation procedure is slightly different for
    bookmarks dataset

    Parameters:
    dataset: Label of current dataset selected by user
    dataset_filtered_data (dict): Dict of data for a particular dataset, with keys being document ID and values being associated data

    Returns:
    regionwise_data (dict): Dict of data with keys being region label and value being regionwise data for that label
    """

    regionwise_data = {}

    if dataset == "bookmarks":
        for img in dataset_filtered_data.values():
            
            if img["bookmarkIndex"] == -1:
                continue

            region = img["regions"][img["bookmarkIndex"]]

            try:    
                if region["regionLabel"] not in regionwise_data.keys():
                    regionwise_data[region["regionLabel"]] = [region]
                else:
                    regionwise_data[region["regionLabel"]].append(region)
            except TypeError:
                pass
        
        regionwise_data["Full Document"] = []

        for img in dataset_filtered_data.values():
            regionwise_data["Full Document"].append(img)

        return regionwise_data
    

    for img in dataset_filtered_data.values():
        for region in img["regions"]:
            try:
                if region["regionLabel"] not in regionwise_data.keys():
                    regionwise_data[region["regionLabel"]] = [region]
                else:
                    regionwise_data[region["regionLabel"]].append(region)
            except TypeError:
                pass
    
    regionwise_data["Full Document"] = []

    for img in dataset_filtered_data.values():
        regionwise_data["Full Document"].append(img)

    return regionwise_data

def sort_regiondata(sort_by,order,selected_region_data):
    """
    Sorts data by user-selected metric, along with the user selected ordering (ascending or descending)

    Parameters:
    sort_by (string): Label of user selected metric they wish to sort the data by
    order (string): Order in which the user wants to sort the data (ascending/descending)
    selected_region_data (list): List of all regions for a user-selected region label

    Returns:
    sorted_data (list): List of data for a user-selected region sorted by the user selected metric which is used for navigation through
    the data 
    """    
    if sort_by == "None":
        return selected_region_data

    if order == "ascending":
        sorted_data = sorted(selected_region_data,key=lambda k: k["metrics"][sort_by],reverse=False)
    else:
        sorted_data = sorted(selected_region_data,key=lambda k: k["metrics"][sort_by],reverse=True)

    return sorted_data

def display_metrics(currData):
    """
    Formats metric data for the current region being shown to user 

    Parameters:
    currData (dict): Current data of the region being shown

    Returns:
    metricStr (string): Formatted string with the metric values of the current region being shown to the user
    """
    metricStr = []
    for metric in currData["metrics"].keys():
        metricStr.append("{}:  {:.4f}".format(metric,currData["metrics"][metric]))
    
    return "    ,    ".join(metricStr)

def bookmark_current_image(bookmarks,document_id,document_data,region_data=None,full_document=False):
    """
    Bookmarks the data passed when the user clicks "bookmark"
    Since bookmarks can be made either regionwise or full document-wise, the data generation procedure is slightly different for full 
    document data

    Parameters:
    bookmarks (dict): Current bookmarks dict of the user's session
    document_id (string): ID associated with the current data being visualized
    document_data (dict): Document data associated with the current data being visualized
    region_data (dict)(optional): Data of current region being visualized, not required to be passed for full document save
    full_document (bool)(optional): Boolean for whether the bookmark is to be made for a full document or region data,
    not required to be passed for regionwise bookmark
    """
    if full_document:
        bookmarks[document_id] = document_data
        bookmarks[document_id]["bookmarkIndex"] = -1
    else:
        bookmarks[document_id] = document_data
        bookmarks[document_id]["bookmarkIndex"] = document_data["regions"].index(region_data)
    
    return bookmarks


def save_current_image(save_path,document_id,document_data=None,region_data=None,full_document=False):
    """
    Writes the current region data to a text file when the user clicks save
    For full document, the id of the document is stored
    For region data, the id of the full document is stored along with the index of the current region

    Parameters:
    save_path (string): Path of where to save the data to, obtained from metaData
    document_id (string): ID of the current full document associated with the current output
    document_data (dict)(optional): Data of the full document being shown, not required to be passed for full document save
    region_data (dict)(optional): Data of the current region being shown, not required to be passed for full document
    full_document (bool)(optional): Whether the save is for a full document or region data, not required to be passed for region save

    Returns:
    None
    """

    if full_document:
        with open(save_path+"/save.txt","a") as f:
            f.write("id: "+str(document_id)+"\n\n")
    
    else:
        with open(save_path+"/save.txt","a") as f:
            f.write("id: "+str(document_id)+"\t, region: "+str(document_data["regions"].index(region_data))+"\n\n")

def get_document_id(currData,dataset_selected_data):
    """
    Gets the ID of the full document data passed

    Parameters:
    currData (dict): Data of the current full document being visualized
    dataset_selected_data (dict): Data of the current dataset selected, stored document-wise

    Returns:
    key_list[pos] (string): ID of the full document data passed
    """
    
    key_list = list(dataset_selected_data.keys())
    val_list = list(dataset_selected_data.values())

    pos = val_list.index(currData)

    return key_list[pos]

def app(metaData):
    """ 
    Main app which renders the layout of the current page selected by the user

    Parameters:
    metaData (dict): Contains the metadata associated with the current layout

    Returns:
    None
    """

    # Key value for the current page layout to avoid conflicts with the other pages of the same layout type (box-supervised layout in this case)

    key = metaData["metaData"]["key"]
    data,outputMasks,defaultDisplayed = get_json_data(metaData["metaData"])

    # Gets current state of app, so that session variables such as counter are preserved after the app restarts

    state = SessionState._get_state()

    # Initializing state variables for current session

    if state.fa_counter is None:
        state.fa_counter = {}
    if key not in state.fa_counter.keys():
        state.fa_counter[key] = 0

    if state.fa_outputs_locked_region is None:
        state.fa_outputs_locked_region = {}

    if key not in state.fa_outputs_locked_region.keys():    
        temp = {}

        for output_type in outputMasks.keys():
            temp[output_type+"-polygon"] = False
            temp[output_type+"-pts"] = False

            if outputMasks[output_type]:

                temp[output_type+"-mask"] = False

                if defaultDisplayed is not None:
                    for d in defaultDisplayed:
                        temp[d] = True            
        
        state.fa_outputs_locked_region[key] = temp

    if state.fa_outputs_locked_document is None:
        state.fa_outputs_locked_document = {}

    if key not in state.fa_outputs_locked_document.keys():    
        temp = {}

        for output_type in outputMasks.keys():
            temp[output_type+"-polygons"] = False
            temp[output_type+"-pts"] = False

            if outputMasks[output_type]:                
                temp[output_type+"-mask"] = False

                if defaultDisplayed is not None:
                    for d in defaultDisplayed:
                        temp[d] = True
        
        state.fa_outputs_locked_document[key] = temp
    
    if state.fa_bookmarks is None:
        state.fa_bookmarks = {}
    if key not in state.fa_bookmarks.keys():
        state.fa_bookmarks[key] = {}

    # MAIN APP LAYOUT

    datasets = list(data.keys())

    # Initializing bookmarks in the list of datasets once the user has bookmarked an image

    if "bookmarks" not in data.keys() and len(list(state.fa_bookmarks[key].keys())) > 0:
        datasets.append("bookmarks")
        data["bookmarks"] = state.fa_bookmarks[key]

    dataset_selected = st.sidebar.selectbox('Select dataset',datasets)
    
    dataset_filtered_data = filter_by_dataset(dataset_selected,data)

    region_data = organize_regions(dataset_selected,dataset_filtered_data)
    
    if state.fa_region is None:
        state.fa_region = {key:list(region_data.keys())[0]}
    elif key not in state.fa_region.keys():
        state.fa_region[key] = list(region_data.keys())[0]
    
    try:
        state.fa_region[key] = st.selectbox(
            'Select region label',
            list(region_data.keys()),
            index=list(region_data.keys()).index(state.fa_region[key])
        )
    except ValueError:
        state.fa_region[key] = st.selectbox(
            'Select component type ',
            list(region_data.keys()),
            index=0
        )

    selected_region_data = region_data[state.fa_region[key]]

    metrics_list = ["None"] 
    
    if "metrics" in selected_region_data[0].keys():
        metrics_list += list(selected_region_data[0]["metrics"].keys())

    sort_by = st.sidebar.selectbox(
        'Sort by (metrics)',
        metrics_list
    )

    order = st.sidebar.selectbox(
        'Sort Order',
        ('ascending','descending')
    )

    with st.sidebar.beta_expander("Display Options"):
        st.markdown("Region Display Options")
        
        for k,v in state.fa_outputs_locked_region[key].items():
            state.fa_outputs_locked_region[key][k] = st.checkbox(label=k,value=v,key="fauto1")
        
        st.markdown("Document Display Options")
        
        for k,v in state.fa_outputs_locked_document[key].items():
            state.fa_outputs_locked_document[key][k] = st.checkbox(label=k,value=v,key="fauto2")

    sorted_data = sort_regiondata(sort_by,order,selected_region_data)

    # Index selection and navigation

    fa_sl = st.empty()

    if len(sorted_data)-1 > 0:
        state.fa_counter[key] = fa_sl.slider("Select image",0,len(sorted_data)-1,state.fa_counter[key])

    c1,c2,_ = st.beta_columns([1,1,8])

    p = c1.button('Previous',key="fauto1")
    n = c2.button('Next',key="fauto1")

    if p:
        state.fa_counter[key] -= 1

    if n:
        state.fa_counter[key] += 1

    if state.fa_counter[key] < 0:
        st.warning("Please select an index value greater than 0")
        state.fa_counter[key] = 0
    elif state.fa_counter[key] > len(sorted_data)-1:
        st.warning("Please select an index value within the range of possible values")
        state.fa_counter[key] = len(sorted_data)-1
    
    currData = sorted_data[state.fa_counter[key]]

    # Display plot and relevant data based on index selected

    if "collection" in currData:
        st.info("This image is taken from the collection: "+currData["collection"])

    if state.fa_region[key] != "Full Document":

        try:
        
            st.write("Region Output")

            regionImage = PlotImage.FullyAutomaticRegionImage(data[dataset_selected][currData["id"]]["imagePath"],currData,outputs_locked=state.fa_outputs_locked_region[key],outputMasks = outputMasks)
            regionImageFig = regionImage.renderImage()
            st.plotly_chart(regionImageFig)

            if "metrics" in selected_region_data[0].keys():
                metricStr = display_metrics(currData)
                st.write(metricStr)

            st.write("Full Document Output")
            
            docImage = PlotImage.FullDocumentImage(data[dataset_selected][currData["id"]],regionShown=currData,outputs_locked=state.fa_outputs_locked_document[key],outputMasks=outputMasks)
            docImageFig = docImage.renderImage()
            st.plotly_chart(docImageFig)

            f_c1,_,f_c2 = st.beta_columns([3,0.1,20])

            if dataset_selected == "bookmarks":

                if f_c1.button("Save 💾",key="fauto1"):
                    save_current_image(metaData["metaData"]["savePath"],currData["id"],document_data=data[dataset_selected][currData["id"]],region_data=currData)
                
                if f_c2.button("Save All 💾",key="fauto2"):
                                    
                    for k,v in state.fa_bookmarks[key].items():                    
                        save_current_image(metaData["metaData"]["savePath"],k,document_data=data[dataset_selected][k],region_data=v["regions"][v["bookmarkIndex"]])
            
            
            else:
                if f_c1.button("Bookmark 🔖",key="fauto2"):
                    state.fa_bookmarks[key] = bookmark_current_image(state.fa_bookmarks[key],currData["id"],data[dataset_selected][currData["id"]],region_data=currData)

                if f_c2.button("Save 💾",key="fauto1"):
                    save_current_image(metaData["metaData"]["savePath"],currData["id"],document_data=data[dataset_selected][currData["id"]],region_data=currData)

        except:
            if "imagePath" not in data[dataset_selected][currData["id"]]:
                st.error("\"imagePath\" missing from data")
            if "groundTruth" not in currData:
                st.error("\"groundTruth\" missing from data")


    else:

        try:
        
            st.write("Full Document Output")
            
            docImage = PlotImage.FullDocumentImage(currData,outputs_locked=state.fa_outputs_locked_document[key],outputMasks=outputMasks)
            docImageFig = docImage.renderImage()
            st.plotly_chart(docImageFig)

            if "metrics" in selected_region_data[0].keys():
                metricStr = display_metrics(currData)
                st.write(metricStr)

            f_c1,_,f_c2 = st.beta_columns([3,0.1,20])

            if dataset_selected == "bookmarks":
                
                if f_c1.button("Save 💾",key="fauto1"):
                    save_current_image(metaData["metaData"]["savePath"],get_document_id(currData,data[dataset_selected]),full_document=True)
                
                if f_c2.button("Save All 💾",key="fauto2"):
                    
                    for k,v in state.fa_bookmarks[key].items():
                        save_current_image(metaData["metaData"]["savePath"],k,full_document=True)


            
            else:

                if f_c1.button("Bookmark 🔖",key="fauto2"):
                    state.fa_bookmarks[key] = bookmark_current_image(state.fa_bookmarks[key],get_document_id(currData,data[dataset_selected]),currData,full_document=True)


                if f_c2.button("Save 💾",key="fauto1"):
                    save_current_image(metaData["metaData"]["savePath"],get_document_id(currData,data[dataset_selected]),full_document=True)

        except:

            if "imagePath" not in currData:
                st.error("\"imagePath\" missing from data")
            
            st.error("There may be an issue with the format of data for a single region")


    # Sync data for all components after updation of a single component to avoid rollbacks

    state.sync()
