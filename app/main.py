import os
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image
from apply import predict_image
from flask import Flask, jsonify, request, abort, Response

app = Flask(__name__)


@app.route('/predict',  methods=['POST'])
def predict():
    # img_data_base64 = request.args.get('img_data')
    params = request.get_json()
    print(params)
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
        return Response(jsonify({"result": res_label}), mimetype='application/json')


@app.route('/')
def index():
    return "hello world"


@app.route('/test_api', methods=['POST'])
def test_api():
    test_name = request.args.get('name')
    return jsonify({"name": test_name})


if __name__ == '__main__':
    allowed_ip_addr = "0.0.0.0"
    access_port = int(os.environ.get('PORT', 80))
    app.run(host=allowed_ip_addr, port=access_port, debug=True)
