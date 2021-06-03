import streamlit as st
import base64


def loadGif(key,index,ocr):
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