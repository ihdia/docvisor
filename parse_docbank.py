from uuid import uuid4 
import json
import cv2 as cv
from tqdm import tqdm
import pdfplumber

def format_data(filepaths,datapath):

    data = {}
    for filepath in filepaths:
        with open(filepath+".txt","r") as f:
            lines = f.readlines()

        getkey = str(uuid4()).replace('-', '')
        print(getkey)
        data[getkey] = {}
        data[getkey]["imagePath"] = filepath+"_ori.jpg"
        data[getkey]["regions"] = []

        page_no = int(filepath.split("_")[-1])
        print(page_no)

        pdf = pdfplumber.open("_".join(filepath.split("_")[:-1]) + "_black.pdf")
        this_page = pdf.pages[page_no]

        width = this_page.width
        height = this_page.height

        img = cv.imread(data[getkey]["imagePath"])
        img = cv.resize(img,(int(width),int(height)))
        cv.imwrite(filepath+"_ori.jpg",img)

        for line in lines:
            temp = {}
            l = line.split("\t")


            x0 = int(l[1])
            y0 = int(l[2])
            x1 = int(l[3])
            y1 = int(l[4])

            x0, y0, x1, y1 = int(x0 * width / 1000), int(y0 * height / 1000), int(x1 * width / 1000), int(y1 * height / 1000)           

            temp["outputs"] = {}
            temp["groundTruth"] = [[int(x0),int(y0)],[int(x1),int(y0)],[int(x1),int(y1)],[int(x0),int(y1)]]
            temp["regionLabel"] = l[9]
            temp["id"] = getkey

            data[getkey]["regions"].append(temp)

    with open(datapath,"w") as f:
        json.dump(data,f)
# how to use the function
format_data(["DocBank_samples/DocBank_samples/246.tar_1808.08720.gz_conll2018_3","docbank_data.json")
