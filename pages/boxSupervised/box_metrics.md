---
title: Metrics
sidebar: mydoc_sidebar
permalink: box_metrics.html
folder: boxSupervised
summary: Description of Metrics in Box Supervised Region Parsing layout.
keywords: metrics
---

### Sorting by metrics during navigation

If the data has metrics computed for the region data, the user can sort the data being served in ascending or descending order according to that metric. However, if there is any metric that is present for one region, that metric must be present in all regions. Refer to [Layout Setup](box_setup.html#data-files) for more information on the format of the data.

Once selected, the region images served during navigation will be in the order of that metric. These can be selected under the `Sort By` and `Sort Order` dropdowns. In addition, There is a default `None` option in the cases where the user may not have metrics to sort the data by.

![metrics gif](gifs/box_metrics.gif)

For those images which have metrics values present in the data, the values are displayed as text below the visualization plot. 