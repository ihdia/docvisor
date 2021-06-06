---
title: Diff Visualizer
keywords: ocr-layout,DocVisor,diff-visualizer
last_updated: June 4, 2021
# tags: [getting_started]
summary: "This page will help you understand the diff Visualizer component of the OCR Layout tool."
sidebar: mydoc_sidebar
permalink: ocr_diffVisualizer.html
folder: ocr
---

{% include note.html content="Note that you can make use of this component only if you have atleast ground truth and one prediction or you have atleast 2 model output predictions" %}

## Ground Truth vs Model

In the OCR setting, our goal is to train our models such that the predicted text is as close to the ground truth. Sometimes, it might be useful to visualize the exact characters that have been wrongly predicted by our models. To do so the OCR tool has provided a diff visualizer.

The gif below should help understand how to use the feature.


![Gif displaying how to change the image highlight color](gifs/gt_vs_model.gif)


## Model Truth vs Model

When you have outputs from multiple models, you may want to see the difference of two strings between those two models. The OCR layout provides a mechanism to do so.




![Gif displaying how to change the image highlight color](gifs/model_vs_model.gif)

## Notation

The above visualization, depicts the minimal operations
required to convert the target string to the reference string. Notice that every
distinct color bounded-text is also annotated with numbers. Also notice that for a
color bounded component in the reference string with annotation i, there could be a corresponding
color bounded text annotated with the same number i in the target string. (the color of these two color-bounded texts need not be the same).

|Color of reference Component i |Color of Target Component i|What does it Mean?|
|---|---|----|
|<span style="background-color:lightgreen">'<some-reference-text\>(i)' </span>|<span style="background-color:lightgreen">'<some-target-text\>(i)' </span>|Component i of reference and component i of the target are **Equal**|
|<span style="background-color:#8C44DB">'<some-reference-text\>(i)' </span>|non-existent|**Insert** Component i of reference after component i-1 of target|
|non-existent|<span style="background-color:#B5651D">'<some-target-text\>(i)' </span>|**Delete** Component i of target|
|<span style="background-color:lightblue">'<some-reference-text\>(i)' </span>|<span style="background-color:orange">'<some-target-text\>(i)' </span>|**Replace** component i of target with component i of reference|


