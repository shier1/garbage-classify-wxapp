import os
import cv2
import base64
import numpy as np
from apply import predict_image
from flask import Flask,Response, jsonify, request

app = Flask(__name__)




@app.route('/predict',  methods=['post'])
def predict():
    img_data_base64 = request.POST.get("img_data")
    img_data = base64.b64decode(img_data_base64) 
    nparr = np.fromstring(img_data,np.uint8)
    img = cv2.imdecode(nparr,cv2.COLOR_BGR2RGB)
    res_label = predict_image(img)
    return jsonify({"result":res_label})

# @app.route('/')
# def index():
#     return "hello world"

if __name__ == '__main__':
    allowed_ip_addr = "0.0.0.0"
    access_port = int(os.environ.get('PORT', 80))
    app.run(host=allowed_ip_addr, port=access_port, debug=True,
            threaded=True, use_reloader=False)