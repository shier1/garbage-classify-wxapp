import os
import cv2
import base64
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from apply import predict_image
from flask import Flask, jsonify, abort, Response, request

app = Flask(__name__)


@app.route('/predict',  methods=['POST'])
def predict():
    params = request.get_json()
    img_data_base64 = params['img_data']
    byte_data = base64.b64decode(img_data_base64)
    # deal the base64 datas lossed the image shape
    img_data = BytesIO(byte_data)
    img_data = Image.open(img_data)
    img = cv2.cvtColor(np.asarray(img_data), cv2.COLOR_RGB2BGR)
    try:
        res_label = predict_image(img)
    except:
        abort(404)
    else:
        return jsonify({"result": res_label})

    
@app.route('/mobilenetv2_cbam',  methods=['POST'])
def mobilenetv2_cbam():
    params = request.get_json()
    img_url = params['img_url']
    print(img_url)
    img_bytes = requests.get(url=img_url)
    
    # deal the base64 datas lossed the image shape
    img_data = BytesIO(img_bytes.content)
    img_data = Image.open(img_data)
    img = cv2.cvtColor(np.asarray(img_data), cv2.COLOR_RGB2BGR)
    print(img.shape)
    try:
        res_label = predict_image(img)
    except:
        abort(404)
    else:
        return jsonify({"result": res_label})
    
@app.route('/')
def index():
    return "hello world"


@app.route('/test_api', methods=['POST'])
def test_api():
    test_params = request.get_json()
    test_name = test_params['name']
    return jsonify({"name": test_name})


if __name__ == '__main__':
    allowed_ip_addr = "0.0.0.0"
    access_port = int(os.environ.get('PORT', 80))
    app.run(host=allowed_ip_addr, port=access_port, debug=True)
