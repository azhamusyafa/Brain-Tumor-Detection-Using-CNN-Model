from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import matplotlib.pyplot as plt
from skimage import filters
import numpy as np
import tensorflow as tf

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Load model
model = tf.keras.models.load_model('model2.h5')
classes = ['Glioma', 'Meningioma', 'Notumor', 'Pituitary']

def get_suggestion(prediction):
    """Memberikan suggestion berdasarkan hasil prediksi."""
    suggestions = {
        'Notumor': '''Based on the analysis, no tumor was detected in the brain scan. However, for complete assurance, we recommend:<br><br>
• Regular follow-up scans as recommended by your healthcare provider<br>
• Maintaining detailed records of any symptoms<br>
• Consulting with a neurologist for comprehensive evaluation''',
        
        'Glioma': '''The scan indicates characteristics of a Glioma. We recommend immediate follow-up steps:<br><br>
• Urgent consultation with a neuro-oncologist<br>
• Additional MRI scans with contrast for detailed tumor mapping<br>
• Discussion of treatment options including surgery, radiation, or chemotherapy''',
        
        'Pituitary': '''Analysis suggests a Pituitary tumor. Recommended next steps include:<br><br>
• Endocrinological evaluation for hormone level assessment<br>
• Consultation with a pituitary specialist<br>
• Additional imaging studies for precise tumor sizing''',
        
        'Meningioma': '''The scan shows patterns consistent with Meningioma. Suggested follow-up actions:<br><br>
• Neurosurgical consultation to discuss treatment options<br>
• Regular monitoring of tumor size and growth rate<br>
• Assessment of any pressure symptoms on surrounding structures'''
    }
    return suggestions.get(prediction, 'Unable to provide suggestion for this prediction.')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """Preprocessing gambar sebelum dimasukkan ke model."""
    image = cv2.imread(image_path)
    image = cv2.resize(image, (128, 128))
    image = image / 255.0  # Normalisasi
    image = np.expand_dims(image, axis=0)
    return image

def predict_tumor(image_path):
    """Prediksi tumor menggunakan model."""
    processed_image = preprocess_image(image_path)
    prediction = model.predict(processed_image)
    predicted_class = classes[np.argmax(prediction)]
    return predicted_class

def apply_canny(image_path):
    """Deteksi tepi menggunakan algoritma Canny."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    result_path = os.path.join(app.config['RESULT_FOLDER'], 'edges.png')
    cv2.imwrite(result_path, edges)
    return result_path

def plot_histogram(image_path):
    """Analisis histogram intensitas."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.hist(gray.ravel(), bins=256, range=[0, 256])
    plt.title('Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    result_path = os.path.join(app.config['RESULT_FOLDER'], 'histogram.png')
    plt.savefig(result_path)
    plt.close()
    return result_path

def segment_image(image_path):
    """Segmentasi area penting menggunakan threshold Otsu."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = filters.threshold_otsu(gray)
    binary = gray > thresh
    result_path = os.path.join(app.config['RESULT_FOLDER'], 'segmentation.png')
    cv2.imwrite(result_path, (binary * 255).astype(np.uint8))
    return result_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def uploaded_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Panggil fungsi untuk melakukan prediksi dan menghasilkan gambar
        prediction = predict_tumor(filepath)
        edge_result = apply_canny(filepath)
        histogram_result = plot_histogram(filepath)
        segment_result = segment_image(filepath)
        
        # Dapatkan suggestion berdasarkan prediksi
        suggestion = get_suggestion(prediction)

        # Kirimkan nama file gambar yang diupload ke halaman result
        return render_template(
            'result.html',
            uploaded_image=filename,  # Nama file gambar yang diupload
            prediction=prediction,
            suggestion=suggestion,
            edge_image=edge_result,
            histogram_image=histogram_result,
            segment_image=segment_result
        )

@app.route('/results/<filename>')
def send_result_file(filename):
    # Memastikan file yang diminta ada di folder uploads atau results
    if filename in os.listdir(app.config['UPLOAD_FOLDER']):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)