import cv2
from flask import Flask, Response, send_file
import numpy as np
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Camera Server"

@app.route('/single_frame')
def single_frame():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    camera.release()

    if not ret:
        return "Could not get frame", 400

    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = bytearray(buffer)

    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    temp_file.write(jpg_as_text)
    temp_filename = temp_file.name
    temp_file.close()

    return send_file(temp_filename, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
