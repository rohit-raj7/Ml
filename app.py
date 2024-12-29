import os
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

app = Flask(__name__)

# Set up the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the pre-trained model
model = load_model('model/cifar10_model.h5')
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Preprocess the image
    image = load_img(filepath, target_size=(32, 32))  # CIFAR-10 images are 32x32
    image = img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    # Make predictions
    predictions = model.predict(image)
    class_idx = np.argmax(predictions)
    class_name = classes[class_idx]

    # Return the result
    return jsonify({'class': class_name, 'confidence': f'{predictions[0][class_idx] * 100:.2f}%'})

if __name__ == '__main__':
    app.run(debug=True)
