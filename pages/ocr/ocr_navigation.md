---
title: Navigation
keywords: ocr-layout,DocVisor,navigation,sorting,metrics,multiple-models
last_updated: June 4, 2021
# tags: [getting_started]
summary: "This page should help the user understand all the possible ways, he can navigate through his dataset so that he/she can be analyze the dataset in a focused manner."
sidebar: mydoc_sidebar
permalink: ocr_navigation.html
folder: ocr
---

## Metrics

{% include note.html content="Note that you can make use of this component only if you have provided metrics as a part of the data in the json file. For more details of how to load the data, visit [this page](/ocr_layout.html)" %}

- The user can navigate based on the metrics provided either by ascending or descending order of the mertics. 
- To do so, use the side navigation bar to select by which metric and how the metric should be sorted for navigation.
- In case you have multiple model outputs, the user can also select by which model's metric the sorting should be done.
- In order to view the metrics in the same order as provided in the json data file, choose the metric "None" using the drop down provided for choosing the metrics.

## Bookmarks

In order to bookmark an image, for further analysis, click the bookmark button at the bottom of the page. Once you have bookmarked all the images, select bookmark in the sidebar navigation from the **Select Dataset Class** section of the drop down. Your image is already bookmarked if there is a 🔖 symbol next to the Image title.

The below gif should help you understand the bookmarks feature:

![Gif displaying how to use the bookmarks feature](gifs/bookmarks.gif)

## Save

To save the particular image index on disk for further analysis, click the save button on the bottom of the image. The index will be saved to disk. To know if your image is already saved, look for the 💾 symbol agains the title IMAGE above your line image.

While navigating through your bookmarks, you can choose to either save a single image onto disk or all bookmarks onto disk at once.

The navigation will save a folder with the following structure:

```
Date/
└── N
    ├── Box-supervised Region Parsing
    │   └── BoundaryNet
    ├── Fully Automatic Region Parsing
    │   ├── DocBank
    │   ├── FullyAutomatic
    │   └── PubTab
    │       
    └── OCR
        ├── OCR-Handwritten
        └── OCR-Printed
            └── save.txt

```

N : Nth time you have used the docVisor tool on that particular date.

## Info

If you have provided the info key in the json data, you will find a info field at the bottom of the page. Expand it to see all the key,value pairs provided in the info field to the ocr layout printed.


![Gif displaying how to see the meta-information of a particular image](gifs/info.gif)
