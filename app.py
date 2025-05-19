import cv2
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Color Detection App", layout="centered")

# Load color data
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

colors = load_colors()

# Find the closest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    closest_name = "Unknown"

    for i in range(len(colors)):
        try:
            r = int(colors.loc[i, "R"])
            g = int(colors.loc[i, "G"])
            b = int(colors.loc[i, "B"])
            d = abs(R - r) + abs(G - g) + abs(B - b)
            if d < minimum:
                minimum = d
                closest_name = colors.loc[i, "color_name"]
        except:
            continue  # Skip rows with invalid data

    return closest_name

# App UI
st.title("🎨 Color Detection from Image")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert to OpenCV format
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    st.markdown("### Step 1: Enter Pixel Coordinates (X and Y)")

    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input("X (Horizontal)", min_value=0, max_value=image.width - 1, step=1)
    with col2:
        y = st.number_input("Y (Vertical)", min_value=0, max_value=image.height - 1, step=1)

    if st.button("Detect Color"):
        pixel = img_cv[int(y), int(x)]
        B, G, R = int(pixel[0]), int(pixel[1]), int(pixel[2])
        color_name = get_color_name(R, G, B)

        st.success(f"🎯 Detected Color: `{color_name}`")
        st.write(f"**RGB Values:** ({R}, {G}, {B})")

        st.markdown("### Color Preview")
        st.markdown(
            f"<div style='width:100px;height:50px;background-color:rgb({R},{G},{B});"
            f"border:1px solid #000;border-radius:5px;'></div>",
            unsafe_allow_html=True
        )
else:
    st.info("📤 Please upload an image to begin.")
@st.cache_data
def load_colors():
    df = pd.read_csv("colors.csv")
    df = df.dropna(subset=["R", "G", "B"])  # drop rows missing RGB
    df = df[df[["R", "G", "B"]].applymap(lambda x: str(x).isdigit())]  # keep numeric-only
    return df
