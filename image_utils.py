import cv2
import time
import numpy as np

def detect_objects(frame, model_weights, model_config):
    # Load the NanoDet model
    net = cv2.dnn.readNet(model_weights, model_config)

    # Preprocess the frame as needed (resize, normalization, etc.)
    # Make sure the frame dimensions match the input size expected by NanoDet

    # Detect objects
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (416, 416), (127.5, 127.5, 127.5), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    detected_objects = []

    for detection in detections[0, 0]:
        confidence = detection[2]
        if confidence > 0.5:
            label = "Something"  # Use a generic label for detected objects
            score = confidence

            x, y, w, h = detection[3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)

            detected_objects.append({
                "label": label,
                "score": score,
                "bounding_box": (x1, y1, x2, y2)
            })

    return detected_objects




def take_snapshot(image_name):
    # Initialize the camera
    camera = cv2.VideoCapture(0)  # Use 0 for the default camera (usually the Raspberry Pi camera)

    # Allow the camera to warm up
    time.sleep(2)

    # Capture a single frame
    ret, frame = camera.read()

    # Save the captured frame to an image file
    if ret:
        file_name = image_name if image_name else time.strftime("%Y%m%d_%H%M%S")
        image_file = f"image_{file_name}.jpg"
        cv2.imwrite(image_file, frame)
        print(f"Image captured and saved as {image_file}")
    else:
        print("Error capturing image")

    # Release the camera
    camera.release()
