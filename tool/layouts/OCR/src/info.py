import streamlit as st

def displayInfo(index,ocr):
    with st.beta_expander('Image Info:'):
        for infokey,infovalue in ocr.JSONdata[index]['info'].items():
            infovalue = ' '.join(infovalue.split('_'))
            st.text(infokey+' : '+infovalue)