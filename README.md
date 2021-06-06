# DocVisor 

DocVisor is an open-source visualization tool. With DocVisor, it is possible to visualize data from three prominent document analysis tasks: Full Document Analysis, OCR and Box-Supervised Region Parsing. DocVisor offers various features such as ground-truth and intermediate output visualization, sorting data by key metrics as well as comparison of outputs from various other models simultaneously.

DocVisor also supports visualization of some common datasets such as [PubTabNet](https://github.com/ibm-aur-nlp/PubTabNet) and [DocBank](https://github.com/doc-analysis/DocBank).

![gif showing text selection in ocr](gifs/textSelectionExample.gif)

![gif showing visualization in fully automatic](gifs/fully-automatic-layout.gif)

![gif showing visualization in box supervised layout](gifs/box-layout.gif)

## How to run DocVisor

1. `pip3 install -r requirements.txt`
2. Run `./run.sh` to launch DocVisor
3. The tool will run on localhost:8501

<!-- For tool's documentation -- kindly visit https://khadiravana-belagavi.github.io/icdar-visualizer/ -->

For the full documentation of DocVisor, visit https://ihdia.iiit.ac.in/docvisor/
