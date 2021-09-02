import layouts.boxSupervision.PlotImage as PlotImage
import SessionState
import streamlit as st
import json
import os

@st.cache(allow_output_mutation=True)
def get_json_data(metaData):
    """
    Fetches the data associated with the current page layout selected from the metadata, along with the optional
    user configuration of which outputs should have masks in the visualization plot

    The function is cached to avoid redundant I/O operations every time page layout is rerun

    Parameters:
    metaData (dict): Contains the metadata associated with the current layout

    Returns:
    data (dict): Key-value pairs of data, with the keys being the datasets and the values being the associated data
    outputMasks (dict): Key-value pairs of data, with the keys being the output label and the values being a bool of whether the output 
    should have a mask representation in the visialization plot
    """

    data = {}

    for dataset in metaData["dataPaths"].keys():

        if "dataFormat" in metaData.keys():
            
            if not os.path.exists("/".join(metaData["dataPaths"][dataset].split("/")[:-1]) + "/" + metaData["dataPaths"][dataset].split("/")[-1].split(".")[0] + "-" + metaData["dataFormat"] + ".json"):
                os.system("python3 parse_"+metaData["dataFormat"]+"_weakly_supervised"+".py "+metaData["dataPaths"][dataset])
        
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
    dataset_filtered_data (list): List of data for a particular dataset
    """

    dataset_filtered_data = data[dataset]
    return dataset_filtered_data

def organize_regions(dataset_filtered_data):
    """
    Creates a dict with keys being region label and associated value being a list of data for that region label

    Parameters:
    dataset_filtered_data (list): List of data for a particular dataset

    Returns:
    regionwise_data (dict): Dict of data with keys being region label and value being regionwise data for that label
    """
    
    regionwise_data = {}

    for img in dataset_filtered_data:
        if img["regionLabel"] not in regionwise_data.keys():
           regionwise_data[img["regionLabel"]] = [img]
        else:
            regionwise_data[img["regionLabel"]].append(img)
    
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

def save_current_image(save_path,currData):
    """
    Writes the current region data to a text file when the user clicks save

    Parameters:
    save_path (string): Path of where to save the data to, obtained from metaData
    currData (dict):  Current data of the region being shown

    Returns:
    None
    """
    with open(save_path+"/save.txt","a") as f:
        f.write(str(currData)+"\n\n")

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

    if state.bookmarks is None:
        state.bookmarks = {}
    if key not in state.bookmarks.keys():
        state.bookmarks[key] = []

    if state.box_counter is None:
        state.box_counter = {}
    if key not in state.box_counter.keys():
        state.box_counter[key] = 0
    
    if state.outputs_locked is None:
        state.outputs_locked = {}
    
    if key not in state.outputs_locked.keys():
        temp = {}
        for output_type in outputMasks.keys():
            temp[output_type+"-polygon"] = False
            temp[output_type+"-pts"] = False

            if outputMasks[output_type]:
                temp[output_type+"-mask"] = False

                if defaultDisplayed is not None:
                    for d in defaultDisplayed:
                        temp[d] = True    
        
        state.outputs_locked[key] = temp

    # MAIN APP LAYOUT

    datasets = list(data.keys())

    # Initializing bookmarks in the list of datasets once the user has bookmarked an image

    if "bookmarks" not in data.keys() and len(state.bookmarks[key]) > 0:
        datasets.append('bookmarks')
        data["bookmarks"] = state.bookmarks[key]

    dataset_selected = st.sidebar.selectbox('Select dataset',datasets)
    dataset_filtered_data = filter_by_dataset(dataset_selected,data)
    region_data = organize_regions(dataset_filtered_data)
    
    if state.region is None:
        state.region = {key:list(region_data.keys())[0]}
    elif key not in state.region.keys():
        state.region[key] = list(region_data.keys())[0]

    
    try:
        state.region[key] = st.selectbox(
            'Select region label',
            list(region_data.keys()),
            index=list(region_data.keys()).index(state.region[key])
        )
    except ValueError:
        state.region[key] = st.selectbox(
            'Select component type ',
            list(region_data.keys()),
            index=0
        )


    selected_region_data = region_data[state.region[key]]

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

        for k,v in state.outputs_locked[key].items():
            state.outputs_locked[key][k] = st.checkbox(label=k,value=v,key="box1")

    sorted_data = sort_regiondata(sort_by,order,selected_region_data)

    # Index selection and navigation

    sl = st.empty()

    if len(sorted_data)-1 > 0:
        state.box_counter[key] = sl.slider("Select image",0,len(sorted_data)-1,state.box_counter[key])

    else:
        state.box_counter[key] = 0

    c1,c2,_ = st.beta_columns([1,1,8])

    p = c1.button('Previous',key="box1")
    n = c2.button('Next',key="box1")

    if p:
        state.box_counter[key] -= 1

    if n:
        state.box_counter[key] += 1

    # Display plot and relevant data based on index selected

    if state.box_counter[key] < 0:
        st.warning("Please select an index value greater than 0")
        state.box_counter[key] = 0
    elif state.box_counter[key] > len(sorted_data)-1:
        st.warning("Please select an index value within the range of possible values")
        state.box_counter[key] = len(sorted_data)-1
    
    currData = sorted_data[state.box_counter[key]]

    if "collection" in currData:
        st.info("This image is taken from the collection: "+currData["collection"]) 

    try:
        region_img = PlotImage.RegionImage(currData,outputMasks,state.outputs_locked[key])
        fig = region_img.renderImage()

        st.plotly_chart(fig)

        metricsStr = display_metrics(currData)
        st.write(metricsStr)
        
        b_c1,_,b_c2 = st.beta_columns([3,0.1,20])

        if dataset_selected == "bookmarks":
            
            if b_c1.button("Save 💾",key="box1"):
                save_current_image(metaData["metaData"]["savePath"],currData)    

            if b_c2.button("Save All 💾",key="box1"):
                
                for b in state.bookmarks[key]:
                    save_current_image(metaData["metaData"]["savePath"],b)                
            
        else:
            
            if b_c1.button("Bookmark 🔖",key="box1"):
                if sorted_data[state.box_counter[key]] not in state.bookmarks[key]:
                    state.bookmarks[key].append(sorted_data[state.box_counter[key]])                                        

            if b_c2.button("Save 💾",key="box1"):
                save_current_image(metaData["metaData"]["savePath"],currData)

    except:
        if "imagePath" not in currData: 
            st.error("\"imagePath\" missing from data")
        if "bbox" not in currData: 
            st.error("\"bbox\" missing from data")
        if "outputs" not in currData:
            st.error("\"outputs\" missing from data")   


    # Sync data for all components after updation of a single component to avoid rollbacks

    state.sync()
