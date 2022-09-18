import os
import cv2
import base64
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from apply import predict_image
from sql import query_exist_user_account, add_user_info, get_db, add_wx_login
from sql import query_forgetpd_question, alter_user_paddword, query_device_url_openid
from sql import query_device_url_account, add_devie_url, add_forgetpd_question
from sql import delete_device_url

from flask import Flask, jsonify, abort, Response, request

app = Flask(__name__)




# @app.route('/check_device_run', methods=["POST"])
# def check_device_run():
#     """
#     检测设备是否运行端口，可以选择去除，内容与下方无异
#     """
#     params = request.get_json()
#     device_url = params['deviceUrl']
#     res = requests.post(device_url)
#     return res
@app.route('/unbind_device', methods=["POST"])
def unbind_device():
    try:
        db = get_db()
        params = request.get_json()
        user_account = params['userAccount']
        device_url = params['deviceUrl']
        openid = params['openid']
        delete_device_url(db=db, device_url=device_url, account=user_account, openid=openid)
    except:
        return jsonify({"unbind_success": False})


@app.route('/get_openid', methods=["POST"])
def get_openid():
    params = request.get_json()
    code = params['code']
    appsecret = "6710d1af63388058b583b9fd851a74c5"
    appid = "wx9b24604931afa738"
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appsecret}&js_code={code}&grant_type=authorization_code&connect_redirect=1"
    res = requests.get(url=url, verify=False)
    return jsonify(res.json())

@app.route('/get_exist_device_openid', methods=["POST"])
def get_exist_device_openid():
    db = get_db()
    params = request.get_json()
    openid = params['openid']
    all_fetched = query_device_url_openid(db, openid)
    result = {"deviceUrl":[], "deviceName":[]}
    for _, _, device_url, device_name in all_fetched:
         result['deviceUrl'].append(device_url)
         result['deviceName'].append(device_name)
    return jsonify(result)


@app.route('/get_exist_device_account', methods=["POST"])
def get_exist_device_account():
    db = get_db()
    params = request.get_json()
    user_account = params['userAccount']
    all_fetched = query_device_url_account(db, user_account)
    result = {"deviceUrl":[], "deviceName":[]}
    for _, _, device_url, device_name in all_fetched:
         result['deviceUrl'].append(device_url)
         result['deviceName'].append(device_name)
    return jsonify(result)


@app.route('/bind_device_openid', methods=["POST"])
def bind_device_openid():
    try:
        db = get_db()
        params = request.get_json()
        device_url = params['deviceUrl']
        openid = params['openid']
        device_name = params['deviceName']
        add_devie_url(db, device_url=device_url, account='', openid=openid, device_name=device_name)
        return jsonify({"bind_success": True})
    except:
        return jsonify({"bind_success": False})


@app.route('/bind_device_account', methods=["POST"])
def bind_device_account():
    try:
        db = get_db()
        params = request.get_json()
        device_url = params['deviceUrl']
        user_account = params['userAccount']
        add_devie_url(db, device_url=device_url, account=user_account, openid='')
        return jsonify({"bind_success":True})
    except:
        return jsonify({"bind_success": False})


@app.route('/get_device_info', methods=["POST"])
def get_device_info():
    params = request.get_json()
    device_url = params['deviceUrl']
    res = requests.post(device_url)
    return jsonify(res.json())


@app.route('/add_user_full', methods=["POST"])
def add_user_full():
    try:
        db = get_db()
        params = request.get_json()
        user_account = params['userAccount']
        question1 = params['question1']
        question2 = params['question2']
        question3 = params['question3']
        add_forgetpd_question(account=user_account, question1=question1, question2=question2, question3=question3)
        return jsonify({"add_success": True})
    except:
        return jsonify({"add_success": False})
        

@app.route('/retrieve_password', methods=["POST"])
def retrieve_password():
    db = get_db()
    params = request.get_json()
    user_account = params['userAccount']
    question1 = params['question1']
    question2 = params['question2']
    question3 = params['question3']
    r_question1, r_question2, r_question3, _ = query_forgetpd_question(db, user_account)
    if(question1 == r_question1 and question2 == r_question2 and question3 == r_question3):
        return jsonify({"retrieve_success": True})
    return jsonify({"retrieve_success": False})


@app.route('/reset_password', methods=["POST"])
def reset_password():
    try:
        db = get_db()
        params = request.get_json()
        user_account  = params['userAccount']
        user_password = params['userPassword']
        alter_user_paddword(db, user_account, user_password)
        return jsonify({"reset_success":True})
    except:
        return jsonify({"reset_success":False})


@app.route('/user_login', methods=['POST'])
def user_login():
    db = get_db()
    params = request.get_json()
    user_account = params['userAccount']
    user_passwd = params['userPassword']
    print(params)
    print(db)
    exist_account = query_exist_user_account(db, account=user_account)
    if exist_account is None:
        return jsonify({"accountNotExist": True, "passwordError": False, "loginSuccess": False})
    elif exist_account[1] == user_passwd:
        return jsonify({"accountNotExist": False, "passwordError": False, "loginSuccess": True})
    else:
        return jsonify({"accountNotExist": False, "passwordError": True, "loginSuccess": False})


@app.route('/user_registry', methods=['POST'])
def user_registry():
    db = get_db()
    params = request.get_json()
    user_account = params['userAccount']
    user_passwd = params['userPassword']
    exist_account = query_exist_user_account(db, account=user_account)
    if exist_account is not None:
        return jsonify({"accountExist": True, "registSuccess": False})
    else:
        add_user_info(db, account=user_account, password=user_passwd)
        return jsonify({"accountExist": False, "registSuccess": True})


@app.route('/wx_login', methods=['POST'])
def wx_login():
    try:
        db = get_db()
        params = request.get_json()
        openid = params['openid']
        add_wx_login(db, openid)
        return jsonify({"wxLoginSuccess":True})
    except:
        return jsonify({"wxLoginSuccess":False})


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
    return "智能垃圾分类箱"



@app.route('/test_api', methods=['POST'])
def test_api():
    test_params = request.get_json()
    test_name = test_params['name']
    return jsonify({"name": test_name})


if __name__ == '__main__':
    allowed_ip_addr = "0.0.0.0"
    access_port = int(os.environ.get('PORT', 80))
    app.run(host=allowed_ip_addr, port=access_port, debug=True)
