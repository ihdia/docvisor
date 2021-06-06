---
title: Getting Started 
keywords: docVisor tool, Contact Points, Contributors
last_updated: May 25, 2021
# tags: [getting_started]
summary: "All necessary instructions to use the DocVisor tool."
sidebar: mydoc_sidebar
permalink: getting_started.html
folder: common
---

## Step 1 : Download or Clone DocVisor tool

### Clone Using Git

If you have git installed on your local machine, run the following command to clone the docvisor repository.

```
git clone https://github.com/ihdia/docvisor
```

### Download Zip

If you do not have git or you want to download the zip file, download the zip file from [here](https://github.com/ihdia/docvisor/archive/refs/heads/main.zip) and unzip the tool to any location on your divice.

## Data Preperation

There three main layouts of the DocVisor tool:

1. Fully Automatic
2. Box Supervised
3. OCR

You can load one or more of these tools to the DocVisor tool at any given point in time.

- To load the Fully Automatic tool, prepare your datafiles as described [here](/fa_setup.html)
- To load the Box Supervised tool, prepare your datafiles as described [here](/box_setup.html)
- To load the OCR tool, prepare your datafiles as described [here](/ocr_layout.html) 


## Setting up your environment

1. Create a conda environment using the following command:

    ```
    conda create --name docvisor
    ```
2. Ensure that the pip points to the docvisor environment by running `which pip`. If it does not, then run the following command:

    ```
    conda install pip
    ```
3. Install the requirements necessary:

   ```
   pip install -r requirements.txt
   ```


## Modify Config File

1. Place all the metaData files in one directory

The metaData directory will look like:

    ```
    metaData/
        - ocr_handwritten.json
        - ocr_printed.json
        - fullyAutomatic.json
        - boxSupervised.json

    ```

2. Change the path of the metaData file in the docvisor/config.py file.


## Launch the tool

Launch the tool by running `./run.sh` script. 


## Load Example Data







