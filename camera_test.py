import cv2
from time import sleep
import numpy as np
import tensorflow as tf
from image_utils import take_snapshot

take_snapshot('captured_image.jpg')

# Load the captured image
image = cv2.imread('captured_image.jpg')

# Resize and preprocess the image based on your model's input requirements
input_shape = (300, 300)  # Adjust based on your model's input size
preprocessed_image = cv2.resize(image, input_shape)
preprocessed_image = preprocessed_image.astype(np.uint8)
preprocessed_image = np.expand_dims(preprocessed_image, axis=0)

#preprocessed_image = preprocessed_image / 255.0  # Normalize pixel values
#preprocessed_image = np.expand_dims(preprocessed_image, axis=0)

interpreter = tf.lite.Interpreter(model_path="lite-model_ssd_mobilenet_v1_1_metadata_2.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()



# Set input tensor
interpreter.set_tensor(input_details[0]['index'], preprocessed_image)

# Run inference
interpreter.invoke()



output_dict = {
    'num_detections': interpreter.get_tensor(output_details[3]["index"]),
    'detection_classes': interpreter.get_tensor(output_details[1]["index"]).astype(np.uint8),
    'detection_scores' : interpreter.get_tensor(output_details[2]["index"])
    }

print(output_dict)






