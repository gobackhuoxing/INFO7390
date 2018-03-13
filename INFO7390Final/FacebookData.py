import requests
import time
import json
import random
import csv
import PhotoProcessor as pp
import PhotoDownloader as pd
import os

token = 'EAACEdEose0cBAK8BIiRkJS3LZBQBC0X7q069RTrSAFaBmBtSScK6MlMQgWhqJLZAzsw4ZChxriafdm46WnDtXWu2O9sm1CHxE02A6g4ZBoZC9iLfGabMLEemjFytUffkCL1DvMBX1bbibvR4kexZC6tI6vL6eMSkVMZAe4d8PToKP4C7OmKiy7ZB3Lyhw78h89gZD'

target = 'steam'
pic_path = 'temp/tempPic.jpg'
result_path = 'temp/FacebookData.csv'

def reqest_facebook(req):
    url = 'https://graph.facebook.com/v2.12/' + req + '?fields=posts.limit(1){picture,message,created_time}&access_token=' + token
    r = requests.get(url)
    return r

result = reqest_facebook(target).json()

data = {}
index = 0

#first post
message = result['posts']['data'][0]['message']
time = result['posts']['data'][0]['created_time']
pictureLink = result['posts']['data'][0]['picture']

print("Downloading image"+str(index))
pd.download_picture(pictureLink,pic_path)
print("Analysing image"+str(index))
picInfo=pp.detect_labels(pic_path)
print("Deleting image"+str(index))
os.remove(pic_path)

data[index] = [time, message, picInfo]
index = index + 1

#second post
r = requests.get(result['posts']['paging']['next'])
result = r.json()
new_messg = result['data'][0]['message']
new_time = result['data'][0]['created_time']
new_picture = result['data'][0]['picture']

print("Downloading image"+str(index))
pd.download_picture(new_picture,pic_path)
print("Analysing image"+str(index))
picInfo=pp.detect_labels(pic_path)
print("Deleting image"+str(index))
os.remove(pic_path)

data[index] = [new_time, new_messg, picInfo]
index = index + 1


##following post
while True:
    try:
        r = requests.get(result['paging']['next'])
        result = r.json()
        new_messg = result['data'][0]['message']
        new_time = result['data'][0]['created_time']
        new_picture = result['data'][0]['picture']

        print("Downloading image"+str(index))
        pd.download_picture(new_picture,pic_path)
        print("Analysing image"+str(index))
        picInfo=pp.detect_labels(pic_path)
        print("Deleting image"+str(index))
        os.remove(pic_path)
        
        data[index] = [new_time, new_messg, picInfo]
        index = index + 1
        
        if index > 100:
            print("100 complate")
            break
    except:
        print("done")
        break
		
myFile = open(result_path, 'w', encoding='utf-8')
with myFile:
    writer = csv.writer(myFile)
    writer.writerow(['created_data', 'Text', 'PictureLabel'])
    for alink in data:
        writer.writerow(data[alink])
		
print("Writing complete")