import cv2
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np

# Load the color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

colors = load_colors()

# Function to get closest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(colors)):
        d = abs(R - int(colors.loc[i, "R"])) + abs(G - int(colors.loc[i, "G"])) + abs(B - int(colors.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = colors.loc[i, "color_name"]
    return cname

st.title("🎨 Image Color Detector")
st.write("Upload an image and click on any point to detect its color.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = np.array(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Click on the image to detect color:")

    click_info = st.image(img, use_column_width=True)

    clicked = st.experimental_data_editor(
        {"Click X": [0], "Click Y": [0]}, 
        num_rows="fixed", 
        key="clickxy", 
        disabled=["Click X", "Click Y"]
    )

    st.write("🔍 Manually enter click position (x, y) for testing:")
    x = st.number_input("X", min_value=0, max_value=img.shape[1]-1, value=0)
    y = st.number_input("Y", min_value=0, max_value=img.shape[0]-1, value=0)

    try:
        b, g, r = img[int(y), int(x)]
        color_name = get_color_name(r, g, b)

        st.markdown(f"### 🎯 Detected Color: **{color_name}**")
        st.markdown(f"**RGB:** ({r}, {g}, {b})")

        # Show color box
        st.markdown(
            f"<div style='width:150px;height:50px;background-color:rgb({r},{g},{b});border-radius:8px;'></div>",
            unsafe_allow_html=True
        )

    except:
        st.error("Invalid click location or image format.")

else:
    st.info("Please upload an image to begin.")

