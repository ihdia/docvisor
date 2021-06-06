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

## Step 2: Prepare your Data

The data file required to launch your OCR layout is a json file. At any given point in time you can visualize a single image and its corresponding ground truth and (multi)-model predictions. Hence the json data provided will be an array of images with
each object of the array having the following format:

```
{
        "id":"<some-unique-image-id>",  # MANDATORY
        "imagePath":"/path/to/line/image/1.jpg", # MANDATORY
        "groundTruth":"annotated-ground-truth-string", 
        "outputs":{
            
            model1,
            model2,
              .   ,
              .   ,
              .   ,
            modeln
        },
        "info":{
            "key1":value1
            "key2":value2
               .     .
               .     .
               .     .
            "keyn":valuen
        }
}
```

1. `id`: 

    - **data-type**: `string`
    - **mandatory**: **YES**
    - **Description**: `id` is a Unique string

2. `imagePath` : 

    - **data-type**: `string`
    - **mandatory**: **YES**
    - **Description**: `imagePath` is a string that has the path to the line image file.

    {% include tip.html content="Give absolute paths as the value to imagePaths." %}

3. `groundTruth` : 

    - **data-type**: `string`
    - **mandatory**: **NO**
    - **Description**: `groundTruth` expects a string. It represents the text ground truth of the line image. This is        **not mandatory**. You can either load the tool with just images or images and predictions if you do not have the ground truth. If passed on, it will be displayed, else it will be omitted. In case you don't have ground truth for your dataset, just ommit the `groundTruth` field.

4. `outputs` : 

    - **data-type**: `dictionary`
    - **mandatory**: **NO**
    - **Description**: If you have outputs of models (with or without attention), you can specify their details in this dictionay. The `outputs` field is not mandatory. In case you just want to load the OCR layout just to analyze the ground truth (for purpose of correction) or just view the images in your dataset, you can ommit the `outputs` field.

    The `outputs` field is a disctionary of models. Each model has the following structure:

    ```
    "model_name":{
            "attentions":[], # array of attentions
            "prediction":"predicted string from the model model_name",
            "metrics":{
                "metric 1": value_1              #value_1 : int,
                "metric 2": value_2             #value_2 : int,
                            .                   
                            .                   
                            .                   
                "metric n": value_n             #value_n : int

            }
    },
    ```
    `model_name` : 
    - **data-type**: `dictionary`
    - **mandatory**: **Yes of there are models, otherwise No**
    - **Description**: Replace the string `model_name` with any unique-name of your interest.


    -
    `attentions`:

    - **data-type**: `list/array`
    - **mandatory**: **NO**
    - **Description**: `attentions` field expects an list of attention numbers. The attentions from your model, should be pre-processed. If you have attentions, you most probably are it getting it as an intermediate output from a Seq2Seq architecture where the attentions are being used by the decoder. We expect that you pre-process the attention matrix such that, for every character of your predicted string, you save the range of the x co-ordinates that your model is attending to for that character. Note that since we are dealing with line images, we only need the x co-ordinates.

        After pre-processing, it is expected that your array be of shape (length_of_your_predicted_sequence,2)After that just ravel that array. i.e. the ith row of your numpy array has the x-co-ordinates of the image (x1,x2) where the model has attended to.
    
        Using the numpy.ravel() command, ravel that array and store and then set it as the value for the `attentions` field.

        Many a times, the sequence predicted and the final sequence displayed is different. For example if you are using some kind of endcoding or your predicted sequence is LaTeX code and you want to visualize the actual compiled output.For the indicOCR case, the sequence predicted was a string of concatenations of the [ords](https://docs.python.org/3.4/library/functions.html?highlight=ord#ord) of each character. So this [line](https://github.com/khadiravana-belagavi/icdar-visualizer/blob/f959c702a8ee75df2749b6f1c99952a624dd7a28/streamlit/layouts/OCR/src/ocrHelper.py#L170) was used for creating the character-Image-pixels mapping. If your encoding structure is different or if you do not have any encoding, feel free to modify/delete the call of `ord` function.

        For more clarification contack `docvisor.iiith@gmail.com`
    
    `predictions`:

    - **data-type**: `string`
    - **mandatory**: **NO**
    - **Description**: Predicted string for that particular model.

    `metrics`:

    - **data-type**: `dictionary`
    - **mandatory**: **NO**
    - **Description**: We expect that there will be metrics if you have both ground truth and predicted text. The metrics is a dictionary with key value pairs. Each key is a string -- name of the metric defined by the user, and value is a number -- integer or float.

    Example of a metrics dictionary:

    ```
        "metrics":{
            "CER":0.12,
            "WER":0.23
        }
    ```
    Where CER and WER correspond to the Character Error Rate and Word Error Rate. You can define your own metrics and load them.

5. `info`:

    - **data-type**: `dictionary`
    - **mandatory**: **NO**
    - **Description**: Many times, our data has some meta information, such as the origin of the file, or which collection it belongs to or any other information. You may even want to have notes on that particular image. So, we have provied the info field which is not mandatory. But if you want to look at individual image's meta information, store the information as key value pairs in a dictionary.

    An example of the `info` key for images taken from classical texts of Indian Languages could be:

    ```
        "info":{
            "collection":"Nirnaya Sindhu"
        }
    ```

    The above info dictionary has a collection key with a value of Nirnaya Sindhu, indicating that the image is taken from the collection Nirnaya Sindhu. You can define your own keys and their corresponding values and any number of them as well. However the values and keys have to be strings. This Information will then be displayed in the bottom of the OCR layout.

The above keys and fields represent data for a single image. To add details of multiple images, store them in the json file as a list.




{% include note.html content="Although you can avoid the non-mandatory fields, the tool expects some form of uniformity. i.e. if a particular non-mandatory field is not present/ is present in the data of the first image, then it should not be present / should be present in all the images of that particular json file." %}

{% include tip.html content="If you have data which is non-uniform, like say, for some images you have ground truth and for others you don't, then classify your dataset such that it is uniform and load each of the classes simultaneously in your metaData file as described [above](#step-11-generation-of-meta-data-file)" %}

   

## Step 3: Launch the Tool

To launch the tool, you need to run the ./run.sh file. The tool will load on localhost with `port 8501`. If `8501` is pre-occupied, check the terminal to know which exact port in which it has been loaded. 


## Help and Feedback

For Feedback or queries, you can either visit the [github repo](https://github.com/ihdia/docvisor) and create issues or use the discussion format. For more details, you can mail, `docvisor.iiith@gmail.com`.









