import io
import os
import csv

from google.cloud import vision
from google.cloud.vision import types

	
def detect_labels(pic_path):
    client = vision.ImageAnnotatorClient()

    with io.open(pic_path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    result=[]
    for label in labels:
        result.append(label.description)
		
    return result

def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)

##pic_path = 'temp/tempPic.jpg'
##path = "temp/result.csv"
##csv_writer(detect_labels(pic_path),path)