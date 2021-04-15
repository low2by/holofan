import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

res = 1.8
step_amount = 0.5

class Stepper():
    def __init__(self):
        Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        Motor1.SetMicroStep("hardware","") #set with DIP switches

    def step_num(self, num):
        Motor1.TurnStep(Dir='forward', steps=num, stepdelay = 0.005)
    
    def step_deg(self, deg):
        steps = deg/res*step_amount
        Motor1.TurnStep(Dir='forward', steps=steps, stepdelay = 0.005)

    def step(self, dir):
        Motor1.step(dir)

    """
    # 1.8 degree: nema23, nema14
    # softward Control :
    # 'fullstep': A cycle = 200 steps
    # 'halfstep': A cycle = 200 * 2 steps
    # '1/4step': A cycle = 200 * 4 steps
    # '1/8step': A cycle = 200 * 8 steps
    # '1/16step': A cycle = 200 * 16 steps
    # '1/32step': A cycle = 200 * 32 steps
    """
    
    Motor1.TurnStep(Dir='forward', steps=800, stepdelay = 0.005)
    time.sleep(0.5)
    Motor1.TurnStep(Dir='backward', steps=800, stepdelay = 0.005)
    Motor1.Stop()
    
except:
    # GPIO.cleanup()
    print("\nMotor stop")
    Motor1.Stop()
    Motor2.Stop()
    exit()