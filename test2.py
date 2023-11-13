from adafruit_servokit import ServoKit
from time import sleep
from utils import RoboticArm

channels = 16
robot = RoboticArm(first_leg_channel=8, second_leg_channel=15, claw_channel=9, channels=16)


try:
    while True:
        limb, angle = input('Give the limp and angle:\n').split()
        angle = int(angle)
        if limb == '1':
            robot.first_leg.angle = angle
        elif limb == '2':
            robot.second_leg.angle = angle
        elif limb == '3':
            robot.claw.angle = angle
        else:
            raise ValueError("Wrong Input")
       
        robot.set_limb_angle(int(limb), int(angle))
except KeyboardInterrupt:
    print('\nTerminating programm')
  
finally:
    robot.cleanup()