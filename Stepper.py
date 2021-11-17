import RPi.GPIO as GPIO
import time
from PololuDriver import PololuDriver

res = 1.8
step_amount = 1

class Stepper():
    def __init__(self):
        self.Motor1 = PololuDriver(dir_pin=26, step_pin=20, enable_pin=21)

    def step_num(self, num, dir='forward'):
        self.Motor1.TurnStep(Dir=dir, steps=num, stepdelay = 0.001)
    
    def step_deg(self, deg, dir='forward'):
        steps = deg/res*step_amount
        self.Motor1.TurnStep(Dir=dir, steps=int(steps), stepdelay = 0.001)

    def step(self, dir='forward'):
        self.Motor1.TurnStep(Dir=dir, steps=1, stepdelay = 0.001)

    
if __name__=="__main__":
        stepper = Stepper()
        while True:
            inp = raw_input()
            if(inp=="f"):
                stepper.step("forward")
            else:
                stepper.step("backward");
        
#         Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
#         Motor1.SetMicroStep("hardware","") #set with DIP switches
# 
#         Motor1.TurnStep(Dir='forward', steps=8, stepdelay = 0.005)
#         time.sleep(0.5)
#         Motor1.TurnStep(Dir='backward', steps=8, stepdelay = 0.005)
#         Motor1.Stop()
