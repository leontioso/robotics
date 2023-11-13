from adafruit_servokit import ServoKit
from time import sleep
from kinetics_utils import RoboticArm
from image_utils import take_snapshot
from object_detection_utils import detect_object

channels = 16
robot = RoboticArm(first_leg_channel=8, second_leg_channel=15, claw_channel=9, channels=16)

#define the box of interest on the image
predefined_box = (0, 260, 800, 800)
image_file = 'tank_photo.jpg'

while True:
    try:
        take_snapshot(image_file)
        sleep(1)
        if detect_object(predefined_box, image_file):
            robot.grab()
        sleep(5)
    except KeyboardInterrupt:
        print('Terminating Program')
        break
    finally:
        robot.cleanup()


