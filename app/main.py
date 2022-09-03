from flask import Flask,Response,render_template
import threading
import cv2


# app = Flask(__name__)


 
# outputFrame = None
# lock = threading.Lock()
 
 
# def detect_motion(frameCount):
#     global vs, outputFrame, lock
 
#     while True:
#         with lock:
#             outputFrame = cv2.imread('app/cdb12.jpg')
#         if 0XFF==27:
#             capture.release()
#             cv2.destoryAllWindows()
#             break

 
 
# def image_to_web():
#     global outputFrame, lock
 
#     while True:
#         with lock:
#             if outputFrame is None:
#                 continue
 
#             (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
 
#             if not flag:
#                 continue
 
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
#                bytearray(encodedImage) + b'\r\n')


# @app.route("/")
# def index():
#     return render_template("index.html")
 


# @app.route("/video_play")
# def video_play():
#     return Response(image_to_web(), mimetype="multipart/x-mixed-replace; boundary=frame")


# if __name__ == '__main__':
#     allowed_ip_addr = "0.0.0.0"
#     access_port = int(os.environ.get('PORT', 80))
 
#     t = threading.Thread(target=detect_motion, args=(24,))
#     t.daemon = True
#     t.start()
 
#     app.run(host=allowed_ip_addr, port=access_port, debug=True,
#             threaded=True, use_reloader=False)

app = Flask(__name__)

@route("/")
def index():
    return "hello world"

if __name__ == "__main__":
    allowed_ip_addr = "0.0.0.0"
    access_port = int(os.environ.get('PORT', 80))
    app.run(host=allowed_ip_addr, port=access_port, debug=True)