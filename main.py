import cv2
from flask import Flask, Response
import numpy as np
import time

app = Flask(__name__)

@app.route('/')
def index():
    return Response(get_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

def get_frame():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        time.sleep(1)  # Delay for 1 second before capturing next frame

    camera.release()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
