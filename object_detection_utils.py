import cv2
from time import sleep
import numpy as np
import tensorflow as tf
import pandas as pd


interpreter = tf.lite.Interpreter(model_path="lite-model_ssd_mobilenet_v1_1_metadata_2.tflite")
with open('labels.txt', 'r') as file:
    class_labels = {int(item.split()[0]):item.split()[1] for item in [line.strip() for line in file.readlines()]}


def detect_object(predefined_box, filename, confidence, area):

    # Load the captured image
    image = cv2.imread(filename)
    imH, imW, _ = image.shape 

    # Resize and preprocess the image based on your model's input requirements
    input_shape = (300, 300)  # Adjust based on your model's input size
    preprocessed_image = cv2.resize(image, input_shape)
    preprocessed_image = preprocessed_image.astype(np.uint8)
    preprocessed_image = np.expand_dims(preprocessed_image, axis=0)




    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], preprocessed_image)


    # Run inference
    interpreter.invoke()

    #minimum confidence score
    min_conf_threshold = confidence

    results = pd.DataFrame(data={
        'ymin' : interpreter.get_tensor(output_details[0]['index'])[0][:, 0],
        'xmin' : interpreter.get_tensor(output_details[0]['index'])[0][:, 1],
        'ymax' : interpreter.get_tensor(output_details[0]['index'])[0][:, 2],
        'xmax' : interpreter.get_tensor(output_details[0]['index'])[0][:, 3],
        'classes' : list(class_labels.get(int(i)) for i in interpreter.get_tensor(output_details[1]['index'])[0]),
        'scores': interpreter.get_tensor(output_details[2]['index'])[0]
    })

    #filtering results
    results = results[(results.scores <= 1.0) &
                      (results.scores >= min_conf_threshold)]


    # normalization of box cords for the draw
    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
    results['ymin'] = (results['ymin'] * imH).apply(lambda x: int(max(x, 1))) 
    results['xmin'] = (results['xmin'] * imW).apply(lambda x: int(max(x, 1)))

    results['ymax'] = (results['ymax'] * imH).apply(lambda x: int(min(x, imH)))
    results['xmax'] = (results['xmax'] * imW).apply(lambda x: int(min(x, imW)))

    # filtering the objects that are inside to the are of interest
    wanted_objects = (results.xmin >= predefined_box[0]) & \
                     (results.ymin >= predefined_box[1]) & \
                     (results.xmax <= predefined_box[2]) & \
                     (results.ymax <= predefined_box[3])
                               

    results = results[wanted_objects]
    
    # filtering the objects considering a predeifined value for size (area)
   
    results = results[(results.xmax - results.xmin) * (results.ymax - results.ymin) <= area]

    print(results)

    cv2.rectangle(image,
            (predefined_box[0], predefined_box[1]),
            (predefined_box[2], predefined_box[3]),
            (0, 0, 0), 2)
    cv2.putText(image,
             "AreaOfInterest",
             ( predefined_box[0], predefined_box[1] + 15),
             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    for row in results.itertuples():
    
        cv2.rectangle(image,
                      (row.xmin,row.ymin),
                      (row.xmax,row.ymax),
                      (10, 255, 0), 2)
        
        label = f'{row.classes}: {int(row.scores*100)}%'  # Example: 'person: 72%'
    
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
        label_ymin = max(row.ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
        cv2.rectangle(image, (row.xmin, label_ymin-labelSize[1]-10), (row.xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
        cv2.putText(image, label, (row.xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
            
    cv2.imwrite(filename.replace('.jpg', '_processed.jpg'), image)
    cv2.destroyAllWindows()
    
    return False if results.empty else True




