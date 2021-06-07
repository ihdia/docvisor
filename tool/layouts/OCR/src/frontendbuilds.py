import streamlit.components.v1 as components
from uuid import uuid4

_roi_selector = components.declare_component("roi_selector",path="tool/layouts/OCR/builds/roiSelectorbuild")
_text_highlighter = components.declare_component("text_highlighter",path="tool/layouts/OCR/builds/textHighlighterbuild")

def roi_selector(img_b64, isEnabled,height, key,default={"start_px":-1,"end_px":-1}):
    default = {"start_px":-1,"end_px":-1,"key":key}
    component_value = _roi_selector(img_b64=img_b64,isEnabled=isEnabled, default=default,key=key)
    return component_value


def text_highlighter(text, ranges, isEnabled,key, default = {"start_idx":-1,"end_idx":-1},font_size=20):
    component_value = _text_highlighter(text=text, ranges=ranges, isEnabled=isEnabled,font_size=font_size, default=default,key=key,key2=str(uuid4()))
    return component_value