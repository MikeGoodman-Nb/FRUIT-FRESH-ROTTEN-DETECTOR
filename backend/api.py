from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

# === ENABLE CORS ===
CORS(app, resources={r"/*": {"origins": "*"}})

# Load model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "fruit_model_fixed.keras")

model = tf.keras.models.load_model(MODEL_PATH)
# model = tf.keras.models.load_model("fruit_model_fixed.keras")

class_names = [
    "freshapples",
    "freshbanana",
    "freshoranges",
    "rottenapples",
    "rottenbanana",
    "rottenoranges"
]

def predict_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, 0)

    pred = model.predict(img_array)
    idx = np.argmax(pred)
    return {
        "class": class_names[idx],
        "confidence": float(pred[0][idx])
    }

@app.route("/predict", methods=["POST"])
def predict_route():
    if "file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    file = request.files["file"]
    result = predict_image(file.read())
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
