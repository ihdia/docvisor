---
title: Layout Setup
sidebar: mydoc_sidebar
permalink: box_setup.html
folder: boxSupervised
summary: Description of how to set up Box Supervised Layout.
keywords: setup
---

## Step 1: Configuring Box Supervised Layout

### Step 1.1 Generation of Meta Data File

The metadata for the box supervised tool essentially acts as a configuration file, through which the user can specify the paths of the json data for the layout, as well as the layout type which the data belongs to (Box Supervised Region Parsing in this case). Additionally, the user can also specify other configuration data for the layout which would be rendered from this metadata, such as whether certain outputs should be shown in the plot with a mask or not. 

Shown below is an example metadata file:

```
{
    "metaData":{
        "pageLayout": "Box-supervised Region Parsing", 
        "pageName": "BoundaryNet", 
        "dataPaths": {
            "Class 1":"/path/to/class_1.json",
            "Class 2":"/path/to/class_2.json",
                    .
                    .
                    .
            "Class N":"/path/to/class_N.json"
        },
        "outputMasks": {"output1":1,"output2":0, ... , "outputN":1},
        "defaultDisplayed": ["output1-polygon","output2-polygon", ... , "outputM-polygon"]

    }
}
```

1. `metaData`:**dict (required)**

    All the relevant data is within the `metaData` attribute of the json data.

2. `pageLayout`:**string (required)**

    `pageLayout` tells the app which layout the data should be rendered in. "box supervised Region Parsing" is the expected value for the data to be rendered in the box supervised Page Layout.

3.  `pageName`:**string (required)**

    `pageName` is the name of the instance of the page layout for the data. Since there can be multiple instances of the same layout for different data, the `pageName` attribute is essential to identify the particular page of interest.

4. `dataPaths`:**dict (required)**

    `dataPaths` is a dictionary with the keys being the name of the group of data (train/test/val for example), and the values are the path to that `json` data. 

5. `outputMasks`:**dict**

    `outputMasks` is a dictionary with the keys `groundTruth` and `modelPrediction`, and their corresponding values a boolean - whether the output should have a mask or not in the visualization plot.

6. `defualtDisplayed`:**list**

    `defaultDisplayed` is a list of all the outputs the user wishes to be displayed and [locked](box_settings.html#display-options) by default. The user should enter the exact output they wish to display. As shown in the example above, the user must provide not just the output to be shown, but also which of the `pts`, `polygon` or  `mask` outputs should be shown.

### Step 1.2 Setup Directory

Create a directory containing only config files. Each instance of the layout should have a json file. For example, if we are trying to visualize data for two box supervised models, the following is a possible directory structure:

```
metadata/
    - boxSupervised_model1.json
    - boxSupervised_model2.json
```

With each of the json files following the format as described above. Note that no two instances of the layout should have the same `pageName` key. 

#### Multiple Layouts

If you are trying to visualize results of either OCR or Fully Automatic Layouts, you can do so, by creating similar metaData files for them as described in their corresponding documentations and then place all of them into this metaData directory.

Example of directory containing all three layouts:

```
metaData/
    - ocr_handwritten.json
    - fullyAutomatic.json
    - boxSupervised.json
```

The docVisor tool will launch single instances of the OCR, Fully Automatic and Box Supervised layouts.

#### Multiple Instances of the Same Layout

The DocVisor tool allows the user to view multiple instances of the same layout in a single session. For example, if you would like to visualize outputs for two box supervised models, as well as a fully automatic layout and an OCR layout, you can just create mulitple a seperate json file with unique `pageName` key and place the file in the metaData directory.

The metaData directory will look like:

```
metaData/
    
    - ocr_handwritten.json
    - fullyAutomatic.json    
    - boxSupervised_model1.json
    - boxSupervised_model2.json

```

For the above directory structure, the DocVisor tool will load two instances of the Box Supervised layout and a single layout of OCR and Fully Automatic layouts.

### Step 1.3: Formatting Data Files

The data files are `json` files which contain the data that is to be visualized. Shown below is an example data file:

```
[
    {
        "imagePath": "/home/user/new_jpg_data/Bhoomi_data/images/AAVARNI VYAKHYA/GOML/991/19.jpg",
        "outputs": {
            "ground_truth": [],
            "gcn_output": [],
            "encoder_output": []
        },
        "metrics": {
            "iou": 0.6072467801928089,
            "hd": 115.10864433221339
        },
        "regionLabel": "Physical Degradation",
        "bbox": [256, 7, 302, 165],
        "collection": "bhoomi"
    }
]
```

The json file with the data for the box-supervised layout is a list of dictionaries. Each dictionary represents the data of a single region of an image . The structure of each dictionary is as follows:

1. `imagePath`:**string (required)**

    `imagePath` is the path to the image of the image associated with the outputs to be visualized. 

2. `outputs`:**dict (required)**

    `outputs` is an dictionary of lists. Each list in turn stores the points of the output polygon to be visualized. In the above example, there are three outputs to be visualized: `ground_truth`, `gcn_output` and `encoder_output`.

3. `metrics`:**dict**

    `metrics` is a dictionary containing the values of all the metrics computed for the data. In the above example, there are two metrics present for the data: `iou` and `hd`.

4. `regionLabel`:**string (required)**

    `regionLabel` contains the label of the region class for the data. In the above example, the `regionLabel` is `Physical Degradation`.

5. `bbox`:**list (required)**

    `bbox` is the user-annotated bounding box for the current region. 

6. `collection`:**string**

    `collection` is additional information such as the collection the current data belongs to in the dataset.


### Step 1.4 Updating the Config File

In tool/config.py file, change the `metaDataDir` to point to the metaData Directory that you have created.


## Step 2: Launch the Tool

To launch the tool, you need to run the ./run.sh file. The tool will load on localhost with `port 8501`. If `8501` is pre-occupied, check the terminal to know which exact port in which it has been loaded. 


## Help and Feedback

For Feedback or queries, you can either visit the [github repo](https://github.com/ihdia/docvisor) and create issues or use the discussion format. For more details, you can mail, `docvisor.iiith@gmail.com.`