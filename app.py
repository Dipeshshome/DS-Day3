from flask import Flask, render_template, request
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import ultralytics
from ultralytics import YOLO

app = Flask(__name__)

# Define the path to your YOLOv8 model file
YOLO_MODEL_PATH = "yolov8n.pt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # Perform YOLOv8 object detection
        result_image_path = run_yolo(file_path)

        return render_template('index.html', result_image=result_image_path)

def run_yolo(image_path):
    # Load YOLOv8 model
    #model = torch.hub.load('.', 'custom', path=YOLO_MODEL_PATH, source='local')
    model = YOLO('best.pt')

    # Perform inference
    results = model.predict(image_path,conf=0.25)

    image = cv2.imread(image_path)
    result_image_path = os.path.join('static', 'results', 'result.jpg')
    for result in results:
        boxes = result.boxes.cpu().xyxy  # Convert boxes to NumPy array
        for box in boxes:
            x1, y1, x2, y2 = box
            cv2.rectangle(image, (int(y1), int(x1)), (int(y2), int(x2)), (0, 255, 0), 2)  # Draw green rectangles

    cv2.imwrite(result_image_path, image)
    return result_image_path

if __name__ == '__main__':
    app.run(debug=True)