import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.set_page_config(page_title="Fruit Freshness Detection")

# ============================================================
# LOAD MODEL
# ============================================================
# Load model .keras versi baru (Keras 3 compatible)
model = tf.keras.models.load_model("fruit_model_fixed.keras")

# Class names sesuai urutan training
class_names = [
    "freshapples",
    "freshbanana",
    "freshoranges",
    "rottenapples",
    "rottenbanana",
    "rottenoranges"
]

# ============================================================
# UI TITLE
# ============================================================
st.title("🍎 Fruit Freshness Detection – SDG 12")
st.write("Upload gambar buah atau gunakan kamera untuk mendeteksi apakah buah masih fresh atau sudah rotten.")

# ============================================================
# INPUT (Upload / Camera)
# ============================================================
uploaded_file = st.file_uploader("Upload gambar buah", type=["jpg", "jpeg", "png"])
camera_file = st.camera_input("Atau gunakan kamera:")

# Tentukan sumber gambar
img_source = uploaded_file if uploaded_file else camera_file

# ============================================================
# RUN PREDICTION
# ============================================================
if img_source:
    # Load gambar dan convert ke RGB
    img = Image.open(img_source).convert("RGB")

    # Tampilkan gambar input
    st.image(img, caption="Gambar Input", width=300)

    # Preprocessing sesuai model
    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 224, 224, 3)

    # Prediksi
    pred = model.predict(img_array)
    idx = np.argmax(pred)
    pred_class = class_names[idx]
    confidence = float(pred[0][idx]) * 100

    # Output
    st.subheader("🔍 Hasil Prediksi")
    st.write(f"**{pred_class}** — {confidence:.2f}% confidence")

    # Logic fresh vs rotten
    if "fresh" in pred_class:
        st.success("Buah ini masih **FRESH** 🍏")
        st.info("Perkiraan buah akan mulai membusuk dalam **2–5 hari** (estimasi sederhana).")
    else:
        st.error("Buah ini **SUDAH ROTTEN** ❌")
