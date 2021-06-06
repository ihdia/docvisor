---
title: Setting Up OCR Layout
keywords: ocr-layout,DocVisor,attention
last_updated: June 4, 2021
# tags: [getting_started]
summary: "This page carries all information required to load the OCR-layout of the DocVisor tool."
sidebar: mydoc_sidebar
permalink: ocr_layout.html
folder: ocr
---


{% include note.html content="Installation of the DocVisor tool is a pre-requisite to be successful in loading the OCR-Layout.  If you have not installed the tool, kindly install the tool following the instructions provided here." %}

To get the tool up and running, the tool requires some metadata files to be ready. The following section should help you set up the metadata files. 

## Step 1 : Configuring the OCR layout

### Step 1.1 Generation of Meta Data File

Meta Data file is a configuration file that tells the OCR Layout of the DocVisor tool the exact location of the datafiles along with other important details. It is in `json` format. The following is an example of what a typical metadata file for the ocr-layout looks like.

```
{
    "metaData": {
        "pageLayout": "OCR",
        "pageName": "Name of your OCR Page Layout",
        "dataPaths": {
            "Class 1": "/path/to/class_1.json",
            "Class 2": "/path/to/class_2.json",
                .               .
                .               .
                .               .
            "Class N":"/path/to/class_n.json"
        }
    }
}
```
1. `pageLayout`: **string**

    The value of `pageLayout` for this page is "OCR". This tells the DocVisor tool to use all the other `metaData`        information and initialize the **OCR** layout of the DocVisor tool. The value of `pageLayout` key can be one of the following:
    1. OCR
    2. Fully Automatic Region Parsing
    3. Box Supervised

    The instructions in this page pertain to setting up and loading OCR(1). Checkout [this link](/fa_setup.html) for 2 and **this link** for 3.
2. `pageName`: **string** 

    `pageName` : Any name of your interest. If you are having multiple OCR-layouts to be loaded, then the `pageName` variable **must** be unique., i.e. no two OCR layout meta data files should have the same `pageName` value.

3. `dataPaths`: **dictionary**

    `dataPaths` is a dictionary having the structure shown above.

    Each key : "class i" is a unique user-defined data class that the user wants to load. A common way of classifying a dataset in most deep learning scenarios is to classify it as *train*, *test* and *validation* sets. The value of each of these "class i" keys is a path to a json data file that has all the ocr data information for that particular class.


Example of Meta Data File:

```
{
    "metaData": {
        "pageLayout": "OCR",
        "pageName": "OCR-Printed",
        "dataPaths": {
            "Train": "/home/user/Desktop/docvisor/train/train_data.json",
            "Validation":"/home/user/Desktop/docvisor/val/val_data.json",
            "Test": "/home/user/Desktop/docvisor/test/test_data.json"
        }
    }
}
```

### Step 1.2 Setup Directory

Create a directory containing only config files. Each instance of the layout should have a json file. For example, if we are trying to visualize the outputs of a line OCR for both typed and hand-written images, the following is the directory structure:

```
metadata/
    - ocr_handwritten.json
    - ocr_printed.json
```

With each of the json files following the format as described above. Note that no two instances of the layout should have the same `pageName` key. 

#### Multiple Layouts

If you are trying to visualize results of either Fully Automatic or Box Supervised Layouts, you can do so, by creating similar metaData files for them as described in their corresponding documentations and then place all of them into this metaData directory.

Example of directory containing all three layouts:

```
metaData/
    - ocr_handwritten.json
    - fullyAutomatic.json
    - boxSupervised.json
```

The docVisor tool will launch single instances of the OCR, Fully Automatic and Box Supervised tools.


#### Multiple Instances of the Same Layout

The DocVisor tool allows the user to view multiple instances of the same layout in a single session. For example, if you have a handwritten dataset and printed dataset and you are wanting to analyze the OCR outputs of both of these datasets, you can just create mulitple a seperate json file with unique `pageName` key and place the file in the metaData directory.

The metaData directory will look like:

```
metaData/
    - ocr_handwritten.json
    - ocr_printed.json
    - fullyAutomatic.json
    - boxSupervised.json

```

For the above directory structure, the DocVisor tool will load two instances of the OCR layout and a single layout of fully automatic and box supervised layouts.

### Step 1.3 Updating the Config File

In docVisor/config.py file, change the `metaDataDir` to point to the metaData Directory that you have created.


## Step 2: Launch the Tool

To launch the tool, you need to run the ./run.sh file. The tool will load on localhost with `port 8501`. If `8501` is pre-occupied, check the terminal to know which exact port in which it has been loaded. 


## Help and Feedback

For Feedback or queries, you can either visit the [github repo](https://github.com/ihdia/docvisor) and create issues or use the discussion format. For more details, you can mail, `docvisor.iiith@gmail.com.`







