import json

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

IMG_SIZE = (224, 224)

st.set_page_config(page_title="Plant Leaf Disease Detection", page_icon="🌿")


@st.cache_resource
def load_model_and_classes():
    model = tf.keras.models.load_model("plant_model.keras")
    with open("class_names.json") as f:
        classes = json.load(f)
    return model, classes


def pretty(name: str) -> str:
    return name.replace("___", " - ").replace("__", " - ").replace("_", " ")


st.title("🌿 Plant Leaf Disease Detection")
st.write("Upload a photo of a single leaf and the model will predict its condition.")

try:
    model, class_names = load_model_and_classes()
except Exception:
    st.error(
        "Model files not found. Run `python train.py` first so that "
        "`plant_model.keras` and `class_names.json` exist in this folder."
    )
    st.stop()

file = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png"])

if file is not None:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="Uploaded leaf", width="stretch")

    arr = np.array(image.resize(IMG_SIZE), dtype="float32")
    arr = np.expand_dims(arr, axis=0)

    with st.spinner("Analysing..."):
        probs = model.predict(arr, verbose=0)[0]

    top = np.argsort(probs)[::-1][:3]
    best = top[0]
    confidence = float(probs[best])

    label = pretty(class_names[best])
    if "healthy" in label.lower():
        st.success(f"**{label}**  ({confidence:.1%} confidence)")
    else:
        st.error(f"**{label}**  ({confidence:.1%} confidence)")

    if confidence < 0.60:
        st.warning(
            "Low confidence. Try a clearer, well-lit photo of a single leaf "
            "against a plain background."
        )

    st.subheader("Top 3 predictions")
    for i in top:
        st.write(pretty(class_names[i]))
        st.progress(float(probs[i]))

st.caption(
    "Trained on the PlantVillage dataset (mostly lab-style leaf photos), so accuracy "
    "can drop on busy field photos. For learning purposes only."
)