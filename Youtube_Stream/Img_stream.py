import requests
import time
import urllib
import get_ip
import json
import subprocess

#FILE INFO
PATH = "snapshot.jpg"

#CAM INFO
IPCAM_TOKEN = '8c585b83-53be92f904af4a6e83f9d1c'
DEVICE_ID = 'FFFFDE8C8D867E29EC642E15FCE34D1D00004492'
url = 'https://use1-wap.tplinkcloud.com/?token=' + IPCAM_TOKEN
data = {"method":"passthrough","params":{"requestData":{"command":"GET_EXTRA_INFO","content":0},"deviceId":DEVICE_ID}}
headers = {'Content-type': 'application/json'}
IP = "0.0.0.0"
attempt = 1

while True:
    while IP == "0.0.0.0":
        print("Attempt " + str(attempt) + ": Finding IP...")
        IP_RESPONSE = requests.post(url, data=json.dumps(data), headers=headers)
        IP = get_ip.from_camera(IP_RESPONSE.text)
        print(IP_RESPONSE.text)
        time.sleep(10)
        attempt = attempt + 1

    print("Camera's IP found: " + IP)
    PORT = '8080'
    USER = 'admin'
    PASS = 'YWRtaW4xMjM0'
    FILENAME = 'snapshot.jpg'
    IMG_PATH='stream/' + FILENAME
    REQUEST_URL = "http://" + USER + ":" + PASS + "@" + IP + ":" + PORT +"/" + IMG_PATH
    SAVE_URL = 'http://admin:uninorte@track-mypower.tk/stream/new?url='

    #INITIATE STREAMING
    while True:
        try:
            try:
                urllib.urlretrieve(REQUEST_URL, FILENAME)
            except:
                break
            post_img = requests.post('http://uploads.im/api?upload', files= dict(fileupload=open(FILENAME, 'rb')))
            img_response = json.loads(post_img.text)
            img_url = str(img_response["data"]["img_url"]).replace('\\', '')
            r=requests.get(SAVE_URL+img_url)
            print(img_url)
            print("-------------------")
            time.sleep(0.4)
        except:
            break
