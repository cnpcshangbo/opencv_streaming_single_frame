import cv2
from flask import Flask, Response, send_file
import numpy as np
import tempfile

app = Flask(__name__)
camera = None  # Declare a global variable for the camera

@app.route('/')
def index():
    return "Welcome to the Camera Server"

@app.route('/single_frame')
def single_frame():
    global camera  # Use the global variable

    if camera is None:  # If the camera is not initialized, initialize it
        camera = cv2.VideoCapture(0)

    ret, frame = camera.read()

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
