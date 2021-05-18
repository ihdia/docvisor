import PlotImage
import SessionState
import streamlit as st
import json

# TODO : replace test back to test data from train data

# Gets current state of app, so that session variables such as counter are preserved after the app restarts

@st.cache(allow_output_mutation=True)
def get_json_data(metaData):

    data = {}

    for dataset in metaData["dataPaths"].keys():
        
        with open(metaData["dataPaths"][dataset],"r") as f:
            loadedData = json.load(f)
        
        data[dataset] = loadedData
    
    if "outputMasks" in metaData.keys():
        outputMasks = metaData["outputMasks"]
    else:
        outputMasks = None

    return data,outputMasks

def filter_by_dataset(dataset,data):

    dataset_filtered_data = data[dataset]
    return dataset_filtered_data

# # Saves current image path, along with IOU and HD values in filenames.txt for later reference

# def save_path(image_path,iou,hd,ttv,index):
#     with open("saved_paths.txt","a") as f:
#         f.write(image_path+"\tiou: "+str(iou)+"\thd: "+str(hd)+"\t"+ttv+"\tindex: "+str(index)+"\n\n")

def organize_regions(dataset_filtered_data):
    
    regionwise_data = {}

    for img in dataset_filtered_data:
        if img["regionLabel"] not in regionwise_data.keys():
           regionwise_data[img["regionLabel"]] = [img]
        else:
            regionwise_data[img["regionLabel"]].append(img)
    
    return regionwise_data

def sort_regiondata(sort_by,order,selected_region_data):
    
    if order == "ascending":
        sorted_data = sorted(selected_region_data,key=lambda k: k["metrics"][sort_by],reverse=False)
    else:
        sorted_data = sorted(selected_region_data,key=lambda k: k["metrics"][sort_by],reverse=True)

    return sorted_data

def display_metrics(currData):
    metricStr = []
    for metric in currData["metrics"].keys():
        metricStr.append("{}:  {:.4f}".format(metric,currData["metrics"][metric]))
    
    return "    ,    ".join(metricStr)

def app(metaData,key,savePath=None):

    data,outputMasks = get_json_data(metaData["metaData"])

    state = SessionState._get_state()

    if state.bookmarks is None:
        state.bookmarks = {key:[]}
    elif key not in state.bookmarks.keys():
        state.bookmarks[key] = []

    if state.counter is None:
        state.counter = {key:0}
    elif key not in state.counter.keys():
        state.counter[key] = 0

    # # MAIN APP LAYOUT

    datasets = list(data.keys())

    if len(state.bookmarks[key]) == 1:
        datasets.append('bookmarks')
    
    data["bookmarks"] = state.bookmarks[key]

    dataset_selected = st.sidebar.selectbox('Select dataset',datasets)
    dataset_filtered_data = filter_by_dataset(dataset_selected,data)
    region_data = organize_regions(dataset_filtered_data)
    
    if state.region is None:
        state.region = {key:list(region_data.keys())[0]}
    elif key not in state.region.keys():
        state.region[key] = list(region_data.keys())[0]

    state.region[key] = st.selectbox(
        'Select component type ',
        list(region_data.keys()),
        index=list(region_data.keys()).index(state.region[key])
    )

    selected_region_data = region_data[state.region[key]]

    sort_by = st.sidebar.selectbox(
        'Sort by (metrics)',
        list(selected_region_data[0]["metrics"].keys())
    )

    order = st.sidebar.selectbox(
        'Sort in ascending or descending order',
        ('ascending','descending')
    )

    sorted_data = sort_regiondata(sort_by,order,selected_region_data)

    # Index selection 

    sl = st.empty()

    if len(sorted_data)-1 > 0:
        state.counter[key] = sl.slider("Select image",0,len(sorted_data)-1,state.counter[key])

    else:
        state.counter[key] = 0

    c1,_,c2 = st.beta_columns([1,10,1])

    p = c1.button('Previous',key="bnet1")
    n = c2.button('Next',key="bnet1")

    if p:
        state.counter[key] -= 1

    if n:
        state.counter[key] += 1

    ind = int(st.text_input("Enter index value here: ",state.counter[key]))
    if ind and ind in range(0,len(sorted_data)):
        state.counter[key] = ind


    # Display image and relevant data based on index selected

    if state.counter[key] < 0:
        st.warning("Please select an index value greater than 0")
        state.counter[key] = 0
    elif state.counter[key] > len(sorted_data)-1:
        st.warning("Please select an index value within the range of possible values")
        state.counter[key] = len(sorted_data)-1
    
    currData = sorted_data[state.counter[key]]

    
    region_img = PlotImage.RegionImage(currData,outputMasks)
    fig = region_img.renderImage()

    st.plotly_chart(fig)

    metricsStr = display_metrics(currData)
    st.write(metricsStr)
    
    b_c1,_,b_c2 = st.beta_columns([1,3,1])

    if b_c1.button("Save for later",key="bnet"):
        # save_path(image_path,iou,hd,dataset_selected,state.counter[key])
        pass

    if b_c2.button("Bookmark 🔖",key="bnet"):
        state.bookmarks[key].append(sorted_data[state.counter[key]])
        pass

    state.sync()
