import streamlit as st

def displayMetrics(ocr,index,model):
    
    no_of_metrics = len(ocr.metric_details[model])

    metricStrings = []
    # st.text(model)
    for  metric in ocr.metric_details[model]:
        if metric !="None":
            mstring = f'**{metric} :** {ocr.JSONdata[index]["outputs"][model]["metrics"][metric]:.2f}'
            metricStrings.append(mstring)

    st.markdown(' , '.join(metricStrings))