from layouts.OCR.src.diffHelper import annotated_text, annotation
import streamlit as st
import difflib

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


def visualizeDiff(key,index,ocr,ref,target,displayImage=False,font_size=30):
    
    # note the order is important:
    # we want to find how to convert predicted to ground
    # not the other way around
    if displayImage:
        imageData = ocr.loadImage(index,ocr.JSONdata)
        if type(imageData)==np.ndarray:
            # if displayImage:
            st.image(imageData)


    if ref!='Ground Truth':
        ground = ocr.JSONdata[index]["outputs"][ref]['prediction']
    else:
        ground = ocr.JSONdata[index]['groundTruth']

    
    predicted = ocr.JSONdata[index]["outputs"][target]['prediction']

    


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


    # if number == 0:
    st.markdown(f"**Reference : ({ref})**")
    annotated_text(
        *groundTextArgs,
        font_size=font_size
    )


    st.markdown(f"**Target : ({target})**")
    annotated_text(
        *predTextArgs,
        font_size=font_size
    )

    with st.beta_expander("diff color-coding notation"):
        st.markdown("""The above visualization, depicts the minimal operations
            required to convert the target string to the reference string. Notice that every
            distinct color bounded-text is also annotated with numbers. Also notice that for a
            color bounded component in the reference string with annotation $i$, there could be a corresponding
            color bounded text annotated with the same number $i$ in the target string. (the color of these two color-bounded texts need not be the same).
        """)
        st.markdown(
            """
            |Color of GT Component $i$ |Color of Predicted Component $i$|What does it Mean?|
            |---|---|----|
            |<span style="background-color:lightgreen">'<some-gt-text\>($i$)' </span>|<span style="background-color:lightgreen">'<some-predicted-text\>($i$)' </span>|Component $i$ of GT and component $i$ of the Prediction are **Equal**|
            |<span style="background-color:#8C44DB">'<some-gt-text\>($i$)' </span>|non-existent|**Insert** Component $i$ of GT after component $i-1$ of Prediction|
            |non-existent|<span style="background-color:#B5651D">'<some-predicted-text\>($i$)' </span>|**Delete** Component $i$ of Prediction|
            |<span style="background-color:lightblue">'<some-gt-text\>($i$)' </span>|<span style="background-color:orange">'<some-predicted-text\>($i$)' </span>|**Replace** component $i$ of Prediction with component $i$ of GT|
            """
        , unsafe_allow_html=True)
