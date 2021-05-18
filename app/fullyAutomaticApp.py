from os import curdir
import streamlit as st
import json
import SessionState
import PlotImage

@st.cache(allow_output_mutation=True)
def get_json_data(metaData):

    data = {}

    for dataset in metaData["dataPaths"].keys():
        
        with open(metaData["dataPaths"][dataset],"r") as f:
            loadedData = json.load(f)
        
        data[dataset] = loadedData
    
    return data

def filter_by_dataset(dataset,data):

    dataset_filtered_data = data[dataset]
    return dataset_filtered_data

def organize_regions(dataset_filtered_data):
    
    regionwise_data = {}

    for img in dataset_filtered_data.values():
        for region in img["regions"]:
            try:
                if region["regionLabel"] not in regionwise_data.keys():
                    regionwise_data[region["regionLabel"]] = [region]
                else:
                    regionwise_data[region["regionLabel"]].append(region)
            except TypeError:
                state = SessionState._get_state()
                
                if state.hide_warning is None or not state.hide_warning:                    
                    st.warning("You have region labels that are not strings, please reformat your data")                
                    state.hide_warning = st.checkbox("Hide Warning")
    
    regionwise_data["Full Document"] = []

    for img in dataset_filtered_data.values():
        regionwise_data["Full Document"].append(img)

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
    data = get_json_data(metaData["metaData"])

    state = SessionState._get_state()

    if state.fa_counter is None:
        state.fa_counter = {key:0}
    elif key not in state.fa_counter.keys():
        state.fa_counter[key] = 0

    # # MAIN APP LAYOUT

    datasets = list(data.keys())

    dataset_selected = st.sidebar.selectbox('Select dataset',datasets)
    
    dataset_filtered_data = filter_by_dataset(dataset_selected,data)

    region_data = organize_regions(dataset_filtered_data)
    
    if state.fa_region is None:
        state.fa_region = {key:list(region_data.keys())[0]}
    elif key not in state.fa_region.keys():
        state.fa_region[key] = list(region_data.keys())[0]
    
    state.fa_region[key] = st.selectbox(
        'Select component type ',
        list(region_data.keys()),
        index=list(region_data.keys()).index(state.fa_region[key])
    )

    selected_region_data = region_data[state.fa_region[key]]
    
    sort_by = st.sidebar.selectbox(
        'Sort by (metrics)',
        list(selected_region_data[0]["metrics"].keys())
    )

    order = st.sidebar.selectbox(
        'Sort in ascending or descending order',
        ('ascending','descending')
    )

    sorted_data = sort_regiondata(sort_by,order,selected_region_data)

    fa_sl = st.empty()

    if len(sorted_data)-1 > 0:
        state.fa_counter[key] = fa_sl.slider("Select image",0,len(sorted_data)-1,state.fa_counter[key])

    c1,_,c2 = st.beta_columns([1,10,1])

    p = c1.button('Previous',key="fauto1")
    n = c2.button('Next',key="fauto1")

    if p:
        state.fa_counter[key] -= 1

    if n:
        state.fa_counter[key] += 1

    fa_ind = int(st.text_input("Enter index value here: ",state.fa_counter[key],key="fauto1"))

    if state.fa_counter[key] < 0:
        st.warning("Please select an index value greater than 0")
        state.fa_counter[key] = 0
    elif state.fa_counter[key] > len(sorted_data)-1:
        st.warning("Please select an index value within the range of possible values")
        state.fa_counter[key] = len(sorted_data)-1
    
    currData = sorted_data[state.fa_counter[key]]

    # displaying image data

    if state.fa_region[key] != "Full Document":

        st.write("Region Output")

        regionImage = PlotImage.FullyAutomaticRegionImage(data[dataset_selected][currData["id"]]["imagePath"],currData)
        regionImageFig = regionImage.renderImage()
        st.plotly_chart(regionImageFig)

        metricStr = display_metrics(currData)
        st.write(metricStr)

        st.write("Full Document Output")
        
        docImage = PlotImage.FullDocumentImage(data[dataset_selected][currData["id"]],regionShown=currData)
        docImageFig = docImage.renderImage()
        st.plotly_chart(docImageFig)
    
    else:

        st.write("Full Document Output")
        
        docImage = PlotImage.FullDocumentImage(currData)
        docImageFig = docImage.renderImage()
        st.plotly_chart(docImageFig)

        metricStr = display_metrics(currData)
        st.write(metricStr)

    if st.button("Save for later",key="bnet"):
        # save_path(image_path,iou,hd,dataset_selected,state.counter)
        pass

    state.sync()



