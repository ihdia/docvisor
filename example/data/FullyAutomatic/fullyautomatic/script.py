import json

with open("test.json","r") as f:
    data = json.load(f)

for k,v in data.items():
    print(v["imagePath"])