---
title: Layout Setup
sidebar: mydoc_sidebar
permalink: fa_setup.html
folder: mydoc
summary: Description of how to set up Fully Automatic Layout.
keywords: setup
---

## Metadata 

The metadata for the fully automatic tool essentially acts as a configuration file, through which the user can specify the paths of the json data for the layout, as well as the layout type which the data belongs to (Fully Automatic Region Parsing in this case). Additionally, the user can also specify other configuration data for the layout which would be rendered from this metadata, such as whether certain outputs should be shown in the plot with a mask or not. The metadata is expected to lie in the `metaData` folder within the `streamlit` folder, and must be a `json` file which follows a specific format.

Shown below is an example metadata file:

```
{
    "metaData":{
        "pageLayout": "Fully Automatic Region Parsing", 
        "pageName": "FullyAutomatic", 
        "dataPaths": {
            "Class 1":"/path/to/class_1.json",
            "Class 2":"/path/to/class_2.json",
                    .
                    .
                    .
            "Class N":"/path/to/class_N.json"
        },
        "outputMasks": {"output1":1,"output2":0, ... , "outputN":1}

    }
}
```

1. `metaData`:**dict**

    All the relevant data is within the `metaData` attribute of the json data.

2. `pageLayout`:**string**

    `pageLayout` tells the app which layout the data should be rendered in. "Fully Automatic Region Parsing" is the expected value for the data to be rendered in the Fully Automatic Page Layout.

3.  `pageName`:**string**

    `pageName` is the name of the instance of the page layout for the data. Since there can be multiple instances of the same layout for different data, the `pageName` attribute is essential to identify the particular page of interest.

4. `dataPaths`:**dict**

    `dataPaths` is a dictionary with the keys being the name of the group of data (train/test/val for example), and the values are the path to that `json` data. 

5. `outputMasks`:**dict**

    `outputMasks` is a dictionary with the keys `groundTruth` and `modelPrediction`, and their corresponding values a boolean - whether the output should have a mask or not in the visualization plot.


## Data Files

The data files are `json` files which contain the data that is to be visualized. Shown below is an example data file:

```
{
    "bhoomi-4422268662325975730":{
        "imagePath":"/data1/hdia_dataset/bhoomi/RGARTHA DIPIKA/GOML/3076/72.jpg",
        "regions":[
            {
                "groundTruth": [], 
                "modelPrediction": [], 
                "regionLabel": "Character Line Segment", 
                "metrics": {
                    "iou": 0.8205464552270203, 
                    "hd": 20.518284528683193
                }, 
                "id": "bhoomi-4422268662325975730",
                "collection": "bhoomi"
            },
            {
                "groundTruth": [], 
                "modelPrediction": [], 
                "regionLabel": "Character Line Segment", 
                "metrics": {
                    "iou": 0.8043249199353717, 
                    "hd": 29.120439557122072
                }, 
                "id": "bhoomi-4422268662325975730",
                "collection": "bhoomi"
            }
        ]
    }
}
```

1. `Document ID`:**string**

    The data is stored on a per-document basis, with an ID being the key for that document's data. In the image shown above, data is shown for only one document. The ID of the document here is `bhoomi-4422268662325975730`.

2. `imagePath`:**string**

    `imagePath` is the path to the image of the document associated with the outputs to be visualized.

3. `regions`:**dict**

    `regions` is an array of dictionaries. Each dictionary in turn stores the regionwise data of the document. Every region which is to be visualized should be present in `regions` in the above format. 

4. 
    1. `groundTruth`:**list**
    2. `modelPrediction`:**list**
    3. `regionLabel`:**string**
    4. `id`:**string**
    5. `metrics`:**dict**
    6. `collection`:**string**

`groundTruth` and `modelPrediction` are lists of points, and are of the form `[[x1,y1],[x2,y2], ... , [xn,yn]]`. `groundTruth` is required, but `modelPrediction` need not exist for every region. Similarly, `regionLabel` and `id` are required, but `metrics` and `collection` are not. `regionLabel` is the region class label for that particular region. `metrics` can have the values of various metrics with which the user can sort the data by during visualization. `collection` is additional information pertaining to the collection from which the document was obtained. 


## Running DocVisor with the Fully Automatic Layout

Once the metadata and data are stored in the correct locations, and in the correct format, DocVisor creates that instance of the layout. This way, the user can have multiple instances of the same page layout.