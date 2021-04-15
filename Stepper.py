import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

res = 1.8
step_amount = 0.5

class Stepper():
    def __init__(self):
        self.Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.Motor1.SetMicroStep("hardware","") #set with DIP switches

    def step_num(self, num):
        self.Motor1.TurnStep(Dir='forward', steps=num, stepdelay = 0.005)
    
    def step_deg(self, deg):
        steps = deg/res*step_amount
        self.Motor1.TurnStep(Dir='forward', steps=steps, stepdelay = 0.005)

    def step(self, dir):
        self.Motor1.TurnStep(Dir=dir, steps=1, stepdelay = 0.005)

    
if __name__=="__main__":
    
    try:
        stepper = Stepper()
        while True:
            stepper.step('forward')
        
#         Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
#         Motor1.SetMicroStep("hardware","") #set with DIP switches
# 
#         Motor1.TurnStep(Dir='forward', steps=800, stepdelay = 0.005)
#         time.sleep(0.5)
#         Motor1.TurnStep(Dir='backward', steps=800, stepdelay = 0.005)
#         Motor1.Stop()
    except:
        # GPIO.cleanup()
#         print("\nMotor stop")
#         Motor1.Stop()
#         Motor2.Stop()
#         exit()
        pass
