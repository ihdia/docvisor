import cv2
import base64
from PIL import Image
import io
import random


def generateInfo():
    
    collections = ['Nirnaya Sindhu','Kavyaprakasha of Mammata','Kshemakutuhalam']

    presentCollection = collections[random.randint(0, 2)]

    

    return collections[random.randint(0, 2)]


def np_to_b64(img_data):
    img_data = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.jpg', img_data)
    pic_str = base64.b64encode(buffer).decode("utf-8")

    img_b64 = "data:image/jpeg;base64, " + pic_str
    imgdata = base64.b64decode(pic_str)
    im = Image.open(io.BytesIO(imgdata))

    return img_b64