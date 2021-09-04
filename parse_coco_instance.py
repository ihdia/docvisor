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

formatted_data = {}

for region in data["annotations"]:
    
    if region["image_id"] not in formatted_data.keys():
    
        temp = {}

        temp["imagePath"] = next((item for item in data["images"] if item["id"] == region["image_id"]),None)["file_name"]

        temp2 = {}
        temp2["groundTruth"] = np.stack((np.array(region["segmentation"][0][::2]),np.array(region["segmentation"][0][1::2])),axis=1)
        temp2["regionLabel"] = next((item for item in data["categories"] if item["id"] == region["category_id"]), None)["name"]
        temp2["id"] = str(region["image_id"])
        temp["regions"] = [temp2]

        formatted_data[region["image_id"]] = temp
    
    else:
        temp2 = {}
        
        # only segmentation of list type supported for now

        if isinstance(region["segmentation"],list):
            temp2["groundTruth"] = np.stack((np.array(region["segmentation"][0][::2]),np.array(region["segmentation"][0][1::2])),axis=1)
        else:
            continue

        temp2["regionLabel"] = next((item for item in data["categories"] if item["id"] == region["category_id"]), None)["name"]
        temp2["id"] = str(region["image_id"])
        temp["regions"] = [temp2]

        formatted_data[region["image_id"]]["regions"].append(temp2)


with open("/".join(sys.argv[1].split("/")[:-1])+"/"+(sys.argv[1].split("/")[-1]).split(".")[0]+"-coco.json","w") as f:
    json.dump(formatted_data,f,cls=NumpyEncoder)

