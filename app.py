from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
JSON_FOLDER = 'json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER

@app.route('/')
def index():
    return 'Hello, this is your Flask API!'

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

@app.route('/draw_boxes/<filename>', methods=['POST'])
def draw_boxes(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    json_path = os.path.join(app.config['JSON_FOLDER'], f"{os.path.splitext(filename)[0]}.json")

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Assume the coordinates are provided in the request as a JSON object
    box_coordinates = request.json.get('boxes', [])

    for box in box_coordinates:
        draw.rectangle(box, outline='red', width=2)

    image.save(image_path)

    with open(json_path, 'w') as json_file:
        json.dump({'boxes': box_coordinates}, json_file)

    return jsonify({'message': 'Boxes drawn and coordinates saved successfully'})

@app.route('/get_image/<filename>')
def get_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['JSON_FOLDER'], exist_ok=True)
    app.run(debug=True)
