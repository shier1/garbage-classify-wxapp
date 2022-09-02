from flask import Flask,Response,render_template
import threading
import cv2
import paddlelite


# initialize a flask object
app = Flask(__name__)


 
outputFrame = None
lock = threading.Lock()
 
# initialize the video stream and allow the camera sensor to
# warmup
capture = cv2.VideoCapture(0)
 
 
def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock
 
    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        ret,frame = capture.read()
        
 
        # lock
        with lock:
            outputFrame = frame.copy()
        if 0XFF==27:
            capture.release()
            cv2.destoryAllWindows()
            break

 
 
def image_to_web():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
 
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
 
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
 
            # ensure the frame was successfully encoded
            if not flag:
                continue
 
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")
 
@app.route("/video_play")
def video_play():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(image_to_web(), mimetype="multipart/x-mixed-replace; boundary=frame")


    # check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    allowed_ip_addr = "0.0.0.0"
    access_port = "8080"
 
    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(24,))
    t.daemon = True
    t.start()
 
    # start the flask app
    app.run(host=allowed_ip_addr, port=access_port, debug=True,
            threaded=True, use_reloader=False)