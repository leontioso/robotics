from adafruit_servokit import ServoKit
from time import sleep

MIN_VAL_FIRST_LEG = 60
MAX_VAL_FIRST_LEG = 180

MIN_VAL_SECOND_LEG = 80
MAX_VAL_SECOND_LEG = 180

MIN_VAL_CLAW = 25
MAX_VAL_CLAW = 100

TIME_INTERVAL = 0.01
STEP_ANGLE = 1


class RoboticArm(ServoKit):
    def __init__(self, first_leg_channel, second_leg_channel, claw_channel,  channels, address=0x40, frequency=60):
        # Create instances of individual limb components
        super().__init__(address=address, frequency=frequency, channels=channels)
        self.first_leg = self.servo[first_leg_channel]
        self.second_leg = self.servo[second_leg_channel]
        self.claw = self.servo[claw_channel]
        self.first_leg.angle, self.second_leg.angle, self.claw.angle = MIN_VAL_FIRST_LEG, MAX_VAL_SECOND_LEG, 80
        
    def move_limp(self, limp, angle):
        if limp == 1 or limp == 'first_leg':
            if int(self.first_leg.angle) < int(angle):
                direction = 1
                angle +=1
            else:
                direction = -1
                angle -= 1
            for i in range(int(self.first_leg.angle), int(angle), STEP_ANGLE * direction):
                if self.second_leg.angle - self.first_leg.angle < 60:
                    self.set_limb_angle(2, self.second_leg.angle - (2 * direction))
                elif angle <= MIN_VAL_FIRST_LEG:
                    self.set_limb_angle(2, MAX_VAL_SECOND_LEG)
                self.first_leg.angle = i
                sleep(TIME_INTERVAL)
            
           
        elif limp == 2 or limp == 'second_leg':
            if int(self.second_leg.angle) < int(angle):
                direction = 1
                angle +=1
            else:
                direction = -1
                angle -= 1
            for i in range(int(self.second_leg.angle), int(angle), STEP_ANGLE * direction):
                self.second_leg.angle = i
                sleep(TIME_INTERVAL)
            
          
        elif limp == 3 or limp == 'claw':
            if int(self.claw.angle) < int(angle):
                direction = 1
                angle += 1
            else:
                direction = -1
                angle -= 1
            for i in range(int(self.claw.angle), int(angle), STEP_ANGLE * direction):
                self.claw.angle = i
                sleep(TIME_INTERVAL)
            
        else:
            raise TypeError('Not a limb')
            
            
        

    def set_limb_angle(self, limb, desir_angle):
        
        if limb == "first_leg" or limb == 1:
            if desir_angle < MIN_VAL_FIRST_LEG:
                self.set_limb_angle(1, MIN_VAL_FIRST_LEG)
            elif desir_angle > MAX_VAL_FIRST_LEG:
                self.set_limb_angle(1, MAX_VAL_FIRST_LEG)
            else:
                self.move_limp(1, desir_angle)
                
             
        elif limb == "second_leg" or limb == 2:
            if desir_angle < MIN_VAL_SECOND_LEG:
                self.set_limb_angle(2, MIN_VAL_SECOND_LEG)
            elif desir_angle > MAX_VAL_SECOND_LEG:
                self.set_limb_angle(2, MAX_VAL_SECOND_LEG)
            else:
                self.move_limp(2, desir_angle)
                
        elif limb == 'claw' or limb==3:
            if desir_angle < MIN_VAL_CLAW:
                self.set_limb_angle(3, MIN_VAL_CLAW)
            elif desir_angle > MAX_VAL_CLAW:
                self.set_limb_angle(3, MAX_VAL_CLAW)
            else:
                self.move_limp(3, desir_angle)
        else:
            raise TypeError('Not a limb')
        
    def grab(self):
        self.set_limb_angle(3, 5)
        
    def release(self):
        self.set_limb_angle(3, 80)
        
        

    def cleanup(self):
        # Call the cleanup methods for all limb components
        self.set_limb_angle(1, MIN_VAL_FIRST_LEG)
        self.set_limb_angle(2, MAX_VAL_SECOND_LEG)
        self.set_limb_angle(3, 80)
        

        
       
    
    