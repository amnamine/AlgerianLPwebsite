from flask import Flask, render_template, request, jsonify, send_file
from ultralytics import YOLO
from PIL import Image
import os
import io

app = Flask(__name__)
model = YOLO('best.pt')
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)
    results = model(img_path)
    result_path = os.path.join(RESULT_FOLDER, 'pred_' + file.filename)
    results[0].save(filename=result_path)
    return send_file(result_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True, port=10000) 