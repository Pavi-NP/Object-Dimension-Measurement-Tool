#obj-dimensions-measurement/app.py

from flask import Flask, render_template, request, jsonify
import os
import base64
from object_dimension_opencv import process_image_from_data, process_file_image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        data = request.json
        
        # Get parameters
        image_data = data.get('image_data')
        threshold = int(data.get('threshold', 100))
        blur_amount = int(data.get('blur_amount', 3))
        pixel_ratio = float(data.get('pixel_ratio', 0.2645833))
        
        # Process the image using OpenCV
        result = process_image_from_data(image_data, threshold, blur_amount, pixel_ratio)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get parameters
        threshold = int(request.form.get('threshold', 100))
        blur_amount = int(request.form.get('blur_amount', 3))
        pixel_ratio = float(request.form.get('pixel_ratio', 0.2645833))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image
        result = process_file_image(filepath, threshold, blur_amount, pixel_ratio)
        
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)