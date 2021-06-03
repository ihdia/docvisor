import jsonlines as jl
from uuid import uuid4 
import json

data = []
with jl.open("/home/user/hdia/hindola/hindola/visualizer/examples/PubTabNet_Examples.jsonl") as f:
    for line in f.iter():
        data.append(line)

formatted_data = {}

for img in data:
    getkey = str(uuid4()).replace('-', '')
    formatted_data[getkey] = {}
    formatted_data[getkey]["imagePath"] = "/home/user/hdia/hindola/hindola/visualizer/examples/"+img["filename"]
    formatted_data[getkey]["regions"] = []

    for region in img["html"]["cells"]:
        temp = {}
        print(region)
       
        try:
            x0,y0,x1,y1 = int(region["bbox"][0]),int(region["bbox"][1]),int(region["bbox"][2]),int(region["bbox"][3])
            temp["groundTruth"] = [[x0,y0],[x1,y0],[x1,y1],[x0,y1],[x0,y0]] 
            temp["regionLabel"] = "region"
            temp["id"] = getkey

            formatted_data[getkey]["regions"].append(temp)
        except:
            pass


    
    print(formatted_data[getkey])

with open("/home/user/hdia/hindola/hindola/visualizer/dev-server/icdar-visualizer/pubtab_data.json","w") as f:
    json.dump(formatted_data,f)
