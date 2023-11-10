from adafruit_servokit import ServoKit
from time import sleep
from utils import RoboticArm

channels = 16
robot = RoboticArm(first_leg_channel=15, second_leg_channel=8, claw_channel=9, channels=16)
print("First leg's angle is: ", robot.first_leg.angle)
print("Second leg's angle is: ", robot.second_leg.angle)
robot.cleanup()
print("First leg's angle is: ", robot.first_leg.angle)
print("Second leg's angle is: ", robot.second_leg.angle)
