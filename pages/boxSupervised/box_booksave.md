---
title: Bookmark and Save
sidebar: mydoc_sidebar
permalink: box_bas.html
folder: boxSupervised
summary: Description of Bookmarking and Saving in Box Supervised Region Parsing layout.
keywords: bookmark, save
---

## Bookmark

During analysis, the user may find an image they would want to come back to later. It would be tedious for the user to have to remember the index of the image, and this is not feasible for a large number of images. Hence, DocVisor offers a bookmarking feature, where the user can bookmark a particular region. The steps would be as follows:

1. Click on the `Bookmark 🔖` button at the bottom of the page.
2. Once you have bookmarked atleast one image, the `bookmarks` option is available under the `Select dataset` dropdown.
3. Users can browse through all the bookmarked images once the `bookmarks` option is selected.

Shown below is a gif of the process. In the gif below, there is an existing bookmark in `bookmarks`, and the user bookmarks another image.

![bookmark gif Box Supervised](gifs/box_bookmark.gif)

## Save

If the user wants to reference the information of a region they are interested in later, bookmarking is only a temporary solution: it only persists for a single session. For that reason, the user can save data of the region. The steps are as follows:

1. Click the `Save 💾` button at the bottom of the page.
2. Once saved, a folder is created for the current date, as well as a number denoting the session of the user. Every new session would create a new folder in the date folder.
3. Within the number folder, three folders `OCR`, `Fully Automatic Region Parsing` and `Box-supervised Region Parsing` can be seen. The desired file will be present in the folder with the name of the instance of the `Box Supervised Region Parsing` layout.

In bookmarks, there is an additional option of being able to `Save All 💾` the bookmarked images.

Shown below is an example of how the directory structure would look for the saved files:

```
31_05_2021/
└── 5
    ├── Box-supervised Region Parsing
    │   └── BoundaryNet
    │       └── save.txt
    ├── Fully Automatic Region Parsing
    │   ├── DocBank
    │   ├── FullyAutomatic
    │   └── PubTab
    └── OCR
        ├── OCR-Handwritten
        └── OCR-Printed
        
```