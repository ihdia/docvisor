---
title: Text to Image Mapping
keywords: ocr-layout,DocVisor,attention,text2Image
last_updated: June 4, 2021
# tags: [getting_started]
summary: "This page will help you understand how to use the Text Selection component of the tool. It will also describe how to use the various settings provided by the OCR-Layout of the DocVisor tool to get a better experience using the text selection component."
sidebar: mydoc_sidebar
permalink: text2Image.html
folder: ocr
---

{% include note.html content="Note that you can make use of this component only if you have provided attentions as a part of the data in the json file. For more details of how to load the data, visit [this page](/ocr_layout.html)" %}

## What is Text to Image Mapping

In the process of learning to map a line image to its corresponding text, in intermediate stage produces the alignment matrix via the attention component. We leverage this attention/alignment matrix to introduce a cool feature of Text to Image and Image to Text Mapping.

## Alignment Matrix

The attentions produced at each time step, can be viewed as a probability distributions indicating the decoder to pay-attention to a certain features of the image. Using this matrix we find the location the model is paying attention at that time step. To see how this is done, visit this page:


## Usage

**Step 1:** In the **Visualize Settings** of the OCR-Layout, select the **Text Selection** Component.

**Step 2:** Select a any substring of the predicted text of **any of the models that have attention** in them. 

**Step 3:** View the highlighted image.

The following gif should give you an idea of the Text Selection Feature and how cool it is.

![Gif displaying how to use the Text Selection Feature](gifs/textSelectionExample.gif)

{% include tip.html content="To know if a model has attentions or not, the OCR-Layout places a *(star symbol) at the end of the name of the tool." %}

## Highlighting Color

If the user wants to change the color used for highlighting the image, to a color that they like or to the one that is best suited for their image dataset, use the tool's sidebar settings to do so.

1. Open the sidebar (if it is not open)
2. Expand the Render component under **Settings**
3. Go to **highlighted image color** and choose the color of your interest.

The tool will now use this color for highlighting the image.

The following gif should help you understand what exactly needs to be done to use this feature.


![Gif displaying how to change the image highlight color](gifs/image_highlight_setting.gif)


## Change Image Threshold

Many times the dataset may have images that are very blurr. For highlighting, we have used an image threshold that best suites a black and white image. However, it is possible that users may have images that are in gray scale, and on selection of a substring of the predicted text, you loose importan character pixels to the highlighted color. To avoid this we have allowed the user to tweak this and set it to a value best for their dataset/purpose.

To do so, follow the below steps:

1. Open the sidebar (if it is not open)
2. Expand the Render component under **Settings**
3. Go to **Image Threshold** and choose the threshold value that bests suits your dataset.

## Text Font Size

For purpose of easy-visualization, users might want to aling text along with the characters in the image. To do so, follow the steps below:

To do so, follow the below steps:

1. Open the sidebar (if it is not open)
2. Expand the Render component under **Settings**
3. Go to **Text Font Size** and choose the font-size value that bests suits the image/dataset.

The following gif should help you understand the feature.

![Gif displaying how to change the text font-size](gifs/font_size_setting.gif)







