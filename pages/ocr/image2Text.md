---
title: Image to Text Mapping
keywords: ocr-layout,DocVisor,attention,image2Text
last_updated: June 4, 2021
# tags: [getting_started]
summary: "This page will help you understand how to use the Image Selection component of the tool. It will also describe how to use the various settings provided by the OCR-Layout of the DocVisor tool to get a better experience using the Image selection component."
sidebar: mydoc_sidebar
permalink: image2Text.html
folder: ocr
---

{% include note.html content="Note that you can make use of this component only if you have provided attentions as a part of the data in the json file. For more details of how to load the data, visit [this page](/ocr_layout.html)" %}

## What is Image to Text Mapping

In the process of learning to map a line image to its corresponding text, in intermediate stage produces the alignment matrix via the attention component. We leverage this attention/alignment matrix to introduce a cool feature of Image to Text Mapping and Text to Image mapping.

## Alignment Matrix

The attentions produced at each time step, can be viewed as a probability distributions indicating the decoder to pay-attention to a certain features of the image. Using this matrix we find the location the model is paying attention at that time step. To see how this is done, visit this page:


## Usage

**Step 1:** In the **Visualize Settings** of the OCR-Layout, select the **Image Selection** Component.

**Step 2:** Select a any sub-portion of the image. 

**Step 3:** View the the corresponding text highlighted on all the models that have attentions provided.

The following gif should give you an idea of the Image Selection Feature and how cool it is.

![Gif displaying how to use the Image Selection Feature](gifs/ImageSelectionExample.gif)

{% include tip.html content="To know if a model has attentions or not, the OCR-Layout places a *(star symbol) at the end of the name of the tool." %}

{% include note.html content="Notice that on selection of a range of the image via a crop like feature, the corresponding the substring of all models that have attentions get highlighted. In the above gif, notice that only indicOCR-v2-C3 and incdicOCR-v2-C1 (which are both conactenated with a * at the end) have their corresponding substrings highlighted. The Google-OCR model, which does not have attentions, will not be able to avail this feature." %}


## Text Font Size

For purpose of easy-visualization, users might want to aling text along with the characters in the image. To do so, follow the steps below:

To do so, follow the below steps:

1. Open the sidebar (if it is not open)
2. Expand the Render component under **Settings**
3. Go to **Text Font Size** and choose the font-size value that bests suits the image/dataset.

The following gif should help you understand the feature.

![Gif displaying how to change the text font-size](gifs/font_size_setting.gif)

Notice that the predicted text words are almost in line with the lines image words, which can help in visualization.







