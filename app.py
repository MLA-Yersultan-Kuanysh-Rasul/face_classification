import os
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model, regularizers
from tensorflow.keras.applications import MobileNetV2
from PIL import Image
import h5py

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Model parameters
IMG_SIZE = (128, 128)  # CRITICAL: Must match training size!
CLASS_NAMES = ["fake", "real"]
MODEL_WEIGHTS_PATH = "model/best_model.h5"
THRESHOLD = 0.42  # Optimal threshold for current model (tested on real data)

# Global model variable
model = None

def load_model():
    global model
    print("Loading model...")
    try:
        model = keras.models.load_model(MODEL_WEIGHTS_PATH, compile=False)
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_augmentation_layer():
    """Returns a Sequential augmentation block."""
    return keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.10),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10),
    ], name="augmentation")

def build_mobilenetv2(learning_rate=1e-3, dropout_rate=0.4, dense_units=256,
                      unfreeze_layers=30, optimizer_name="adam", include_augmentation=True):
    """Build MobileNetV2 model architecture."""
    backbone = MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    backbone.trainable = False

    inputs = keras.Input(shape=(*IMG_SIZE, 3))

    # Only include augmentation during training
    if include_augmentation:
        x = get_augmentation_layer()(inputs)
        x = layers.Rescaling(1.0 / 127.5, offset=-1)(x)
    else:
        x = layers.Rescaling(1.0 / 127.5, offset=-1)(inputs)

    x = backbone(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(dense_units, activation="relu",
                     kernel_regularizer=regularizers.l2(1e-4))(x)
    x = layers.Dropout(dropout_rate)(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = Model(inputs, outputs, name="MobileNetV2_FaceClassifier")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model

def load_model():
    """Load the trained model."""
    global model
    print("Loading model...")

    try:
        # Load model with compile=False to avoid optimizer issues
        model = keras.models.load_model(MODEL_WEIGHTS_PATH, compile=False)

        # Recompile with simple settings for inference
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        print("Model loaded successfully!")

        # Test prediction
        dummy = np.zeros((1, *IMG_SIZE, 3), dtype=np.float32)
        test_pred = model.predict(dummy, verbose=0)
        print(f"Test prediction: {test_pred[0][0]:.4f}")

    except Exception as e:
        print(f"Error loading model: {e}")
        raise

    print("Model ready for inference!")

def preprocess_image(image_path):
    """Preprocess image for prediction."""
    img = Image.open(image_path).convert('RGB')
    img = img.resize(IMG_SIZE)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Preprocess and predict
            img_array = preprocess_image(filepath)
            prediction = model.predict(img_array, verbose=0)[0][0]

            # Convert to percentage
            fake_prob = (1 - prediction) * 100
            real_prob = prediction * 100

            # Determine class using optimal threshold
            predicted_class = CLASS_NAMES[1] if prediction >= THRESHOLD else CLASS_NAMES[0]

            # Confidence is the probability of the predicted class
            confidence = real_prob if predicted_class == "real" else fake_prob

            # Clean up uploaded file
            os.remove(filepath)

            return jsonify({
                'prediction': predicted_class,
                'confidence': float(confidence),
                'fake_probability': float(fake_prob),
                'real_probability': float(real_prob)
            })

        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file type'}), 400

load_model()

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
