import cv2
from time import sleep
import numpy as np
import tensorflow as tf
from image_utils import take_snapshot
import pandas as pd

take_snapshot('captured_image.jpg')

# Load the captured image
image = cv2.imread('captured_image.jpg')
imH, imW, _ = image.shape 

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

with open('labels.txt', 'r') as file:
    class_labels = {int(item.split()[0]):item.split()[1] for item in [line.strip() for line in file.readlines()]}



# Set input tensor
interpreter.set_tensor(input_details[0]['index'], preprocessed_image)


# Run inference
interpreter.invoke()



#results = pd.DataFrame(data = {
#    'box': interpreter.get_tensor(output_details[0]["index"][0]),  
#    'detection_classes': [class_labels.get(int(i)) for i in interpreter.get_tensor(output_details[1]["index"]).astype(np.uint8).flatten()],
#    'detection_scores' : interpreter.get_tensor(output_details[2]["index"][0])
#    })


boxes = interpreter.get_tensor(output_details[0]['index'])[0]
classes = list(class_labels.get(int(i)) for i in interpreter.get_tensor(output_details[1]['index'])[0])
scores = interpreter.get_tensor(output_details[2]['index'])[0]
min_conf_threshold = 0.4


for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            
            cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
            
            object_name = classes[i] # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
            
            cv2.imwrite('captured_image_proccessed.jpg', image)
            

cv2.destroyAllWindows()




