import streamlit as st

def displayModelHeading(text,type):

    if type == 'attention-model':
        text+='*'


    style_def =  "<style>.model-heading {text-decoration: underline ;!important;}</style>"
    st.markdown(style_def, unsafe_allow_html=True)
    st.markdown(f' <h2 class="model-heading"> {text}</h2>',unsafe_allow_html=True)
    if type == 'attention-model':
        st.markdown('')
