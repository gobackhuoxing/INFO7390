import requests
import time
import json
import random
import csv
import re
import string
import time
##import PhotoProcessor as pp
##import PhotoDownloader as pd
import os

token = 'EAACEdEose0cBAJdOiMIP24vFB2PuQvgNZAEzY6BLOmRKX89goGJT2xVvEioeXNbka3ZBQZBW3HHUTi5AZAQV2oL88MQllmTZAZCZCcsqJ2GZAHKgeYys5dAs69rp9oqBvF59519xr04ZARYZA6ExbqtyIujPAUVkDrPQ58hN9vZB6PgJ7vjEEuTpyqJDzuq4FThe6IZD'

datasize = 100
pic_path = 'temp/tempPic.jpg'
result_path = 'temp/FacebookData.csv'

def reqest_facebook(req):
    url = 'https://graph.facebook.com/v2.12/' + req + '?fields=posts.limit(1){picture,message,created_time}&access_token=' + token
    r = requests.get(url)
    return r

data = []
	
def shot_target(target):
    result = reqest_facebook(target).json()

    translation = str.maketrans("","", string.punctuation)
    try:
	    #first post
        message = result['posts']['data'][0]['message']
        message = clean_str(message)
        message = message.translate(translation)
        time = result['posts']['data'][0]['created_time']
        pictureLink = result['posts']['data'][0]['picture']

#        print("Downloading image"+str(index))
#        pd.download_picture(pictureLink,pic_path)
#        print("Analysing image"+str(index))
#        picInfo=pp.detect_labels(pic_path)
#        print("Deleting image"+str(index))
#        os.remove(pic_path)
        print([message,target])
        data.append([message,target])
    except:
	    print("Connection error, skip this post")
		
    #second post
    try:
        r=requests.get(result['posts']['paging']['next'])
        result = r.json()
        new_messg = result['data'][0]['message']
        new_messg = clean_str(new_messg)
        new_messg = new_messg.translate(translation)
        new_time = result['data'][0]['created_time']
        new_picture = result['data'][0]['picture']

#        print("Downloading image"+str(index))
#        pd.download_picture(new_picture,pic_path)
#        print("Analysing image"+str(index))
#        picInfo=pp.detect_labels(pic_path)
#        print("Deleting image"+str(index))
#        os.remove(pic_path)
        print([new_messg,target])   
        data.append([new_messg,target])
    except:
	    print("Connection error, skip this post")
		
    ##following post
    size = len(data)
    while True:
        try:
            r = requests.get(result['paging']['next'])
            result = r.json()
            new_messg = result['data'][0]['message']
            new_messg = clean_str(new_messg)
            new_messg = new_messg.translate(translation)
            new_time = result['data'][0]['created_time']
            new_picture = result['data'][0]['picture']

#            print("Downloading image"+str(index))
#            pd.download_picture(new_picture,pic_path)
#            print("Analysing image"+str(index))
#            picInfo=pp.detect_labels(pic_path)
#            print("Deleting image"+str(index))
#            os.remove(pic_path)
            print([new_messg,target])
            data.append([new_messg,target])
            if len(data) > size+datasize:
                break
        except:
            print("Connection error, skip this post")
            continue
        

def clean_str(string):
    """
    from: https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)     
    string = re.sub(r"\'s", " \'s", string) 
    string = re.sub(r"\'ve", " \'ve", string) 
    string = re.sub(r"n\'t", " n\'t", string) 
    string = re.sub(r"\'re", " \'re", string) 
    string = re.sub(r"\'d", " \'d", string) 
    string = re.sub(r"\'ll", " \'ll", string) 
    string = re.sub(r",", " , ", string) 
    string = re.sub(r"!", " ! ", string) 
    string = re.sub(r"\(", " \( ", string) 
    string = re.sub(r"\)", " \) ", string) 
    string = re.sub(r"\?", " \? ", string) 
    string = re.sub(r"\s{2,}", " ", string)    
    return string.strip().lower()			
			
def main(target__list):
    for target in target__list:
            shot_target(target)
			
    myFile = open(result_path, 'w', newline='', encoding='utf-8')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(['Text','label'])
        for row in data:
            writer.writerow(row)
    print("Writing complete")
	
target__list= ['steam','microsoft','google']
main(target__list)