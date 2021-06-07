---
title: Visualization
sidebar: mydoc_sidebar
permalink: fa_vis.html
folder: fullyAutomatic
summary: Description of Visualization in Fully Automatic layout.
keywords: visualization
---

## Overview

The main feature of the Fully Automatic layout is the visualization of the model's outputs it enables the user to have. The visualization plot offers a visual comparison to the ground-truth data for the same region, as well as for the entire document. The user can visualize the region in a more focused plot, as well as a full-length plot of the document it belongs to. Additionally, the user can also choose to view only the full-document outputs. Refer to [Navigation](fa_navigation.html) for more information.

The plot is interactive, and the user can select or de-select the outputs (polygons, points and masks). These outputs can be toggled from the legend of the plot, which has the color-coded labels for each output. Double-clicking a single output in the legend would hide all other outputs, and show only the clicked output. Double-clicking on an output twice would display all outputs simultaneously in the plot.

The plot also has features such as zooming in and out, panning and cropping. These options appear in the top-right of the plot, when the user hovers their mouse over it.

Shown below is a gif of how a user would visualize outputs for a region as well as a full document:
![Gif showing visualization in fully automatic layout.](gifs/fully-automatic-layout.gif)

## Region Output

The `Region Output` area of the layout displays the visualization plot for the current region served. In `Full Document`, there is no `Region Output` area. The metrics displayed here (`iou` and `hd` in the image below) are of the region only. 

Shown below is an example of the `Region Output`:

![Region output in fully automatic.](images/fa_region.png)

## Full Document Output

The `Full Document Output` area of the layout displays the visualization plot for the full document which the current region belongs to. The region in a red highlited area is the region being shown above in the `Region Output` area. 

In `Full Document`, the metrics displayed are of the full document. 

Shown below is an example of `Full Document Output` that is displayed along with a `Region Output`:

![Full document output in fully automatic.](images/fa_document.png)

Shown below is an example of `Full Document Output` that is displayed when the user selects `Full Document`:

![Full document output without region in fully automatic.](images/fa_document_full.png)