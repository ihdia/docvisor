import json
import numpy as np
import sys

"""
Assumes ground truth annotation, groundTruth label can be changed according to data.
"""

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

with open(sys.argv[1],"r") as f:
    data = json.load(f)

formatted_data = []

for region in data["annotations"]:
    temp = {}
    temp["imagePath"] = data["images"][region["image_id"]]["file_name"]
    temp["outputs"] = {}
    temp["outputs"]["groundTruth"] = np.stack((np.array(region["segmentation"][0][::2]),np.array(region["segmentation"][0][1::2])),axis=1)
    temp["regionLabel"] = next((item for item in data["categories"] if item["id"] == region["category_id"]), None)["name"]
    temp["bbox"] = region["bbox"]

    formatted_data.append(temp)

with open("/".join(sys.argv[1].split("/")[:-1])+"/"+(sys.argv[1].split("/")[-1]).split(".")[0]+"-coco.json","w") as f:
    json.dump(formatted_data,f,cls=NumpyEncoder)

