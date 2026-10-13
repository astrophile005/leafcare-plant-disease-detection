import hashlib
import io
import json
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps

from knowledge import get_info

IMG_SIZE = (224, 224)
LOW_CONFIDENCE = 0.60
SUPPORTED_CROPS = [
    "Apple", "Blueberry", "Cherry", "Corn", "Grape", "Orange", "Peach",
    "Bell pepper", "Potato", "Raspberry", "Soybean", "Squash", "Strawberry", "Tomato",
]
DISCLAIMER = (
    "LeafCare is a learning project. Its advice is general and is not a substitute for "
    "an agricultural expert. For serious outbreaks, contact your local agriculture office."
)

st.set_page_config(page_title="LeafCare", page_icon="🌿", layout="centered")

# Per-visitor memory (lives until the browser tab is closed or refreshed)
if "history" not in st.session_state:
    st.session_state.history = []
if "scans" not in st.session_state:
    st.session_state.scans = {}


# ---------------------------------------------------------------- model helpers
@st.cache_resource(show_spinner="Loading the model...")
def _load():
    model = tf.keras.models.load_model("plant_model.keras")
    with open("class_names.json") as f:
        classes = json.load(f)
    return model, classes


def get_model():
    try:
        return _load()
    except Exception as e:
        st.error(
            "Could not load the model files. Make sure `plant_model.keras` and "
            "`class_names.json` are in the same folder as app.py."
        )
        st.caption(str(e))
        st.stop()


def predict(image):
    """Return the top 3 (class_name, probability) pairs for a PIL image."""
    model, classes = get_model()
    arr = np.array(image.resize(IMG_SIZE), dtype="float32")[np.newaxis, ...]
    probs = model.predict(arr, verbose=0)[0]
    top = np.argsort(probs)[::-1][:3]
    return [(classes[i], float(probs[i])) for i in top]


def render_details(info):
    """Show the description and advice for a condition."""
    d = info["details"]
    if not d:
        st.info("No detailed notes are available for this condition yet.")
        return
    if info["healthy"]:
        st.markdown("**Keeping it healthy**")
    else:
        st.markdown(f"**Type:** {d['type']}")
        st.markdown(f"**What it looks like:** {d['symptoms']}")
        st.markdown("**What you can do**")
    for action in d["actions"]:
        st.markdown(f"- {action}")


# ------------------------------------------------------------------------ pages
def dashboard_page():
    st.title("🌿 LeafCare")
    st.caption("Plant leaf disease detection, powered by deep learning.")

    hist = st.session_state.history
    df = pd.DataFrame(hist)
    total = len(df)
    diseased = int((~df["Healthy"]).sum()) if total else 0
    healthy = total - diseased
    avg = f"{df['Confidence'].mean():.1f}%" if total else "-"

    row1 = st.columns(2)
    row1[0].metric("Leaves scanned", total)
    row1[1].metric("Diseases found", diseased)
    row2 = st.columns(2)
    row2[0].metric("Healthy leaves", healthy)
    row2[1].metric("Avg. confidence", avg)

    st.page_link(scan_pg, label="Scan a new leaf", icon="🔍")

    if total == 0:
        st.info("No scans yet. Scan your first leaf and your results will appear here.")
    else:
        found = df[~df["Healthy"]]
        if len(found):
            st.subheader("Conditions detected")
            counts = (found["Crop"] + " - " + found["Result"]).value_counts()
            st.bar_chart(counts)
        st.subheader("Recent scans")
        recent = df.drop(columns=["Healthy"]).tail(5)[::-1]
        st.dataframe(recent, hide_index=True, width="stretch")

    st.subheader("About the model")
    st.markdown(
        "- **Accuracy:** 94.64% on 10,876 validation images it never trained on\n"
        "- **Coverage:** 38 classes across 14 crops\n"
        "- **Method:** MobileNetV2 with transfer learning, trained on the PlantVillage dataset"
    )


def scan_page():
    st.title("🔍 Scan a leaf")
    st.caption("Use a clear photo of ONE leaf, ideally on a plain background in good light.")

    mode = st.radio("Add a photo by", ["Uploading", "Using the camera"], horizontal=True)
    if mode == "Uploading":
        file = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png"])
        source = file.name if file else None
    else:
        file = st.camera_input("Take a photo of the leaf")
        source = "Camera photo"

    if file is None:
        st.info(
            "Supported crops: " + ", ".join(SUPPORTED_CROPS) + ". Other plants will be "
            "forced into one of these classes, so results for them are not reliable."
        )
        return

    data = file.getvalue()
    key = hashlib.md5(data).hexdigest()
    image = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    st.image(image, width="stretch")

    if key not in st.session_state.scans:
        with st.spinner("Analysing the leaf..."):
            top = predict(image)
        st.session_state.scans[key] = top
        best, conf = top[0]
        info = get_info(best)
        st.session_state.history.append({
            "Time": datetime.now().strftime("%d %b %Y, %H:%M"),
            "Source": source,
            "Crop": info["crop"],
            "Result": info["condition"],
            "Healthy": info["healthy"],
            "Confidence": round(conf * 100, 1),
        })

    top = st.session_state.scans[key]
    best, conf = top[0]
    info = get_info(best)

    with st.container(border=True):
        st.caption(info["crop"])
        if info["healthy"]:
            st.success(f"✅ {info['condition']}")
        else:
            st.error(f"⚠️ {info['condition']}")
        st.progress(conf, text=f"Confidence: {conf:.1%}")

    if conf < LOW_CONFIDENCE:
        st.warning("Low confidence. Try a clearer photo of a single leaf on a plain background.")

    render_details(info)

    with st.expander("Other possibilities (top 3)"):
        for name, p in top:
            i = get_info(name)
            st.write(f"{i['crop']} - {i['condition']}")
            st.progress(p, text=f"{p:.1%}")

    st.caption(DISCLAIMER)


def library_page():
    st.title("📚 Disease library")
    st.caption("Browse every condition LeafCare can recognise.")

    _, classes = get_model()
    items = [(c, get_info(c)) for c in classes]
    crops = sorted({i["crop"] for _, i in items})

    crop = st.selectbox("Crop", ["All crops"] + crops)
    query = st.text_input("Search", placeholder="e.g. blight, rust, mildew")
    hide_healthy = st.toggle("Hide healthy classes", value=True)

    shown = 0
    for _, i in items:
        if crop != "All crops" and i["crop"] != crop:
            continue
        if hide_healthy and i["healthy"]:
            continue
        if query and query.lower() not in f"{i['crop']} {i['condition']}".lower():
            continue
        shown += 1
        with st.expander(f"{i['crop']} - {i['condition']}"):
            render_details(i)
    if shown == 0:
        st.info("Nothing matches your filters.")
    st.caption(DISCLAIMER)


def history_page():
    st.title("🕑 Scan history")
    hist = st.session_state.history
    if not hist:
        st.info("No scans yet.")
        st.page_link(scan_pg, label="Scan a leaf", icon="🔍")
        return

    df = pd.DataFrame(hist).drop(columns=["Healthy"])[::-1]
    st.dataframe(
        df,
        hide_index=True,
        width="stretch",
        column_config={
            "Confidence": st.column_config.ProgressColumn(
                "Confidence (%)", min_value=0, max_value=100, format="%.1f"
            )
        },
    )
    st.download_button(
        "⬇️ Download as CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="leafcare_history.csv",
        mime="text/csv",
    )
    if st.button("🗑️ Clear history"):
        st.session_state.history = []
        st.session_state.scans = {}
        st.rerun()
    st.caption("History is kept only while this page stays open in your browser.")


def about_page():
    st.title("ℹ️ About LeafCare")
    st.markdown(
        """
**How it works**
1. You upload or take a photo of a leaf.
2. The image is resized to 224 x 224 pixels.
3. A MobileNetV2 neural network, pretrained on ImageNet and fine-tuned on about 54,000
   PlantVillage leaf photos, scores all 38 classes.
4. LeafCare shows the best match, a confidence score, and general advice.

**Limits to keep in mind**
- It only knows 38 classes from 14 crops. Any other plant is forced into one of them.
- The training photos are mostly single leaves on plain backgrounds, so messy field photos
  are harder.
- A high confidence score means "closest match among known classes", not "definitely correct".
"""
    )
    st.caption(DISCLAIMER)


dashboard_pg = st.Page(dashboard_page, title="Dashboard", icon="🏠", default=True)
scan_pg = st.Page(scan_page, title="Scan", icon="🔍")
library_pg = st.Page(library_page, title="Disease library", icon="📚")
history_pg = st.Page(history_page, title="History", icon="🕑")
about_pg = st.Page(about_page, title="About", icon="ℹ️")

st.navigation([dashboard_pg, scan_pg, library_pg, history_pg, about_pg]).run()
