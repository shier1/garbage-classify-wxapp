import requests
import base64
import cv2


data = {}

url = "https://garbage-classify-2187015-1313534064.ap-shanghai.run.tcloudbase.com/predict"
image = cv2.imread('app/cdb12.jpg')
with open('app/cdb12.jpg', 'rb') as f:
    img_data = base64.b64encode(f.read())

data['img_data'] = img_data
res = requests.post(url, data=data)
print(res.json())
