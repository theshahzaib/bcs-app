import streamlit as st
import cv2
import numpy as np

# Add company logo to sidebar
st.sidebar.image("CVNLP-Lab-Logo.png", width=250)

# Create sidebar
st.sidebar.title("More Settings")

algorithm = st.sidebar.selectbox("Algorithm", ["AbsDiff", "Canny Edge Detection", "Thresholding"])

# Add threshold slider
threshold = st.sidebar.slider("Threshold", 0, 255, 25)

# Add blur checkbox
blur = st.sidebar.checkbox("Apply Blur")
poly = st.sidebar.checkbox("Apply Polygons")



def change_detection(img1, img2):
    if algorithm == "AbsDiff":
        # Convert images to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Apply blur if selected
        if blur:
            gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)
            gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)

        # Compute difference between images
        diff = cv2.absdiff(gray1, gray2)

        # Threshold difference image
        thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

        return thresh

    elif algorithm == "Canny Edge Detection":
        # Apply Canny edge detection
        edges1 = cv2.Canny(img1, 100, 200)
        edges2 = cv2.Canny(img2, 100, 200)

        # Compute difference between edges
        diff = cv2.absdiff(edges1, edges2)

        return diff

    elif algorithm == "Thresholding":
        # Convert images to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        thresh1 = cv2.threshold(gray1, threshold, 255, cv2.THRESH_BINARY)[1]
        thresh2 = cv2.threshold(gray2, threshold, 255, cv2.THRESH_BINARY)[1]

        # Compute difference between thresholded images
        diff = cv2.absdiff(thresh1, thresh2)

        return diff

# Create main interface
st.title("Construction Stages Monitoring")

# Upload images
img1 = st.file_uploader("Upload Before Image", type=["jpg", "png", "tif"], help='Upload image files equal in dimentions')
img2 = st.file_uploader("Upload After Image", type=["jpg", "png", "tif"])

# Display images
if img1 and img2:
    img1_bytes = img1.read()
    img2_bytes = img2.read()

    img1 = cv2.imdecode(np.frombuffer(img1_bytes, np.uint8), cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np.frombuffer(img2_bytes, np.uint8), cv2.IMREAD_COLOR)

    st.image(img1, caption="Image 1")
    st.image(img2, caption="Image 2")

    # Run change detection
    result = change_detection(img1, img2)

    # Display result
    st.image(result, caption="Change Detection Result")

# Add copyright notice to footer
st.markdown("Copyright (c) 2024 CENTAIC. All rights reserved. 🚀 Designed by Shahzaib 🔥")