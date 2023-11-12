import cv2
import time
import numpy as np


def take_snapshot(image_name='captured_image.jpg'):
    # Initialize the camera
    camera = cv2.VideoCapture(0)  # Use 0 for the default camera (usually the Raspberry Pi camera)

    # Allow the camera to warm up
    #time.sleep(2)

    # Capture a single frame
    ret, frame = camera.read()

    # Save the captured frame to an image file
    if ret: 
        cv2.imwrite(image_name, frame)
        print(f"Image captured and saved as {image_name}")
    else:
        print("Error capturing image")

    # Release the camera
    camera.release()
