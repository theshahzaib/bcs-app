import gradio as gr
import cv2
import numpy as np

def change_detection(img1, img2, algorithm, threshold, blur):
    if algorithm == "AbsDiff":
        result = cv2.absdiff(img1, img2)
    elif algorithm == "Canny Edge Detection":
        result = cv2.Canny(img1, 100, 200)
    elif algorithm == "Thresholding":
        result = cv2.threshold(img1, threshold, 255, cv2.THRESH_BINARY)[1]

    if blur:
        result = cv2.GaussianBlur(result, (5, 5), 0)

    return result

def blend_images(img1, img2, blend_slider):
    blended_img = cv2.addWeighted(img1, blend_slider, img2, 1 - blend_slider, 0)
    return blended_img

gr.Interface(
    fn=change_detection,
    inputs=[
        gr.Image(label="Image 1"),
        gr.Image(label="Image 2"),
        gr.Dropdown(label="Algorithm", choices=["AbsDiff", "Canny Edge Detection", "Thresholding"]),
        gr.Slider(label="Threshold", minimum=0, maximum=255, value=25),
        gr.Checkbox(label="Apply Blur")
    ],
    outputs=gr.Image(label="Change Detection Result")
).launch()

gr.Interface(
    fn=blend_images,
    inputs=[
        gr.Image(label="Image 1"),
        gr.Image(label="Image 2"),
        gr.Slider(label="Blend", minimum=0.0, maximum=1.0, value=0.5)
    ],
    outputs=gr.Image(label="Blended Image")
).launch()