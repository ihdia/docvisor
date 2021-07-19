---
title: Layout Setup
sidebar: mydoc_sidebar
permalink: fa_setup.html
folder: fullyAutomatic
summary: Description of how to set up Fully Automatic Layout.
keywords: setup
---

## Step 1: Configuring Fully Automatic Layout

### Step 1.1 Generation of Meta Data File

The metadata for the fully automatic tool essentially acts as a configuration file, through which the user can specify the paths of the json data for the layout, as well as the layout type which the data belongs to (Fully Automatic Region Parsing in this case). Additionally, the user can also specify other configuration data for the layout which would be rendered from this metadata, such as whether certain outputs should be shown in the plot with a mask or not.

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
        "outputMasks": {"output1":1,"output2":0, ... , "outputN":1},
        "defaultDisplayed": ["output1-mask","output2-mask", ... , "outputM-mask"]

    }
}
```

1. `metaData`:**dict (required)**

    All the relevant data is within the `metaData` attribute of the json data.

2. `pageLayout`:**string (required)**

    `pageLayout` tells the app which layout the data should be rendered in. "Fully Automatic Region Parsing" is the expected value for the data to be rendered in the Fully Automatic Page Layout.

3.  `pageName`:**string (required)**

    `pageName` is the name of the instance of the page layout for the data. Since there can be multiple instances of the same layout for different data, the `pageName` attribute is essential to identify the particular page of interest.

4. `dataPaths`:**dict (required)**

    `dataPaths` is a dictionary with the keys being the name of the group of data (train/test/val for example), and the values are the path to that `json` data. 

5. `outputMasks`:**dict**

    `outputMasks` is a dictionary with the keys `groundTruth` and `modelPrediction`, and their corresponding values a boolean - whether the output should have a mask or not in the visualization plot.

6. `defualtDisplayed`:**list**

    `defaultDisplayed` is a list of all the outputs the user wishes to be displayed and [locked](fa_settings.html#display-options) by default. The user should enter the exact output they wish to display. As shown in the example above, the user must provide not just the output to be shown, but also which of the `pts`, `polygon` or  `mask` outputs should be shown.

An example instance of the metadata file can be found [here](https://github.com/ihdia/docvisor/blob/main/example/metaData/fullyautomatic_metadata.json)

### Step 1.2 Setup Directory

Create a directory containing only config files. Each instance of the layout should have a json file. For example, if we are trying to visualize data for two fully automatic models, the following is a possible directory structure:

```
metadata/
    - fullyAutomatic_model1.json
    - fullyAutomatic_model2.json
```

With each of the json files following the format as described above. Note that no two instances of the layout should have the same `pageName` key. 

#### Multiple Layouts

If you are trying to visualize results of either OCR or Box Supervised Layouts, you can do so, by creating similar metaData files for them as described in their corresponding documentations and then place all of them into this metaData directory.

Example of directory containing all three layouts:

```
metaData/
    - ocr_handwritten.json
    - fullyAutomatic.json
    - boxSupervised.json
```

The docVisor tool will launch single instances of the OCR, Fully Automatic and Box Supervised layouts.

#### Multiple Instances of the Same Layout

The DocVisor tool allows the user to view multiple instances of the same layout in a single session. For example, if you would like to visualize outputs for two fully automatic models, as well as a box supervised layout and an OCR layout, you can just create mulitple a seperate json file with unique `pageName` key and place the file in the metaData directory.

The metaData directory will look like:

```
metaData/
    
    - fullyAutomatic_model1.json
    - fullyAutomatic_model2.json    
    - ocr_handwritten.json
    - boxSupervised.json

```

For the above directory structure, the DocVisor tool will load two instances of the Fully Automatic layout and a single layout of OCR and Box Supervised layouts.

### Step 1.3: Formatting Data Files

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

1. `Document ID`:**string (required)**

    The data is stored on a per-image basis, with an ID being the key for that image's data. In the image shown above, data is shown for only one image. The ID of the image here is `bhoomi-4422268662325975730`.

2. `imagePath`:**string (required)**

    `imagePath` is the path to the image of the image associated with the outputs to be visualized.

3. `regions`:**dict (required)**

    `regions` is an list of dictionaries. Each dictionary in turn stores the regionwise data of the image. Every region which is to be visualized should be present in `regions` in the above format. 

4. 
    1. `groundTruth`:**list (required)**
    2. `modelPrediction`:**list**
    3. `regionLabel`:**string (required)**
    4. `id`:**string (required)**
    5. `metrics`:**dict**
    6. `collection`:**string**

`groundTruth` and `modelPrediction` are lists of points, and are of the form `[[x1,y1],[x2,y2], ... , [xn,yn]]`. `groundTruth` is required, but `modelPrediction` need not exist for every region. Similarly, `regionLabel` and `id` are required, but `metrics` and `collection` are not. `regionLabel` is the region class label for that particular region. `metrics` can have the values of various metrics with which the user can sort the data by during visualization. `collection` is additional information pertaining to the collection from which the image was obtained. 

Example instances of the json data file can be found [here](https://github.com/ihdia/docvisor/tree/main/example/jsonData/FullyAutomatic/fullyautomatic)

### Step 1.4 Updating the Config File

In tool/config.py file, change the `metaDataDir` to point to the metaData Directory that you have created.


## Step 2: Launch the Tool

To launch the tool, you need to run the ./run.sh file. The tool will load on localhost with `port 8501`. If `8501` is pre-occupied, check the terminal to know which exact port in which it has been loaded. 


## Help and Feedback

For Feedback or queries, you can either visit the [github repo](https://github.com/ihdia/docvisor) and create issues or use the discussion format. For more details, you can mail, `docvisor.iiith@gmail.com.`