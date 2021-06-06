---
title: Metrics
sidebar: mydoc_sidebar
permalink: fa_metrics.html
folder: fullyAutomatic
summary: Description of Metrics in Fully Automatic layout.
keywords: metrics
---

### Sorting by metrics during navigation

If the data has metrics computed for the regions as well as the full document, the user can sort the data being served in ascending or descending order according to that metric. However, if there is any metric that is present for one region/document, that metric must be present in all regions/documents. Refer to [Layout Setup](fa_setup.html#data-files) for more information on the format of the data.

Once selected, the documents served during navigation will be in the order of that metric. These can be selected under the `Sort By` and `Sort Order` dropdowns. In addition, There is a default `None` option in the cases where the user may not have metrics to sort the data by.

![metrics gif](gifs/fa_metrics.gif)

### Metrics displayed for each image

For those images which have metrics values present in the data, the values are displayed as text below the visualization plot. When the data is being visualized per region, the metrics shown are for that region only. On the other hand, when `Full Document` is selected as the region, the metrics shown are naturally for the entire document.