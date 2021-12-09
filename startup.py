#!/usr/bin/env python3
from __future__ import print_function
from encoder_test import Encoder
import subprocess
import odrive
from odrive.enums import *
import time
import math
import signal

def handler(signum, frame):
    my_drive.axis0.config.sensorless_ramp.vel = 0
    my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    exit(1)

encoder = Encoder();

initpos = encoder.readpos() >> 6


currentpos = initpos
flags = 0

while(initpos +  512 > currentpos and initpos - 512 < currentpos):
    time.sleep(0.2)
    temp = encoder.readpos()
    flags = temp&0x3F;
    if(not(flags & 0x20) or flags & 0x10 or flags & 0x04 or flags & 0x08):
        continue
    currentpos = temp >> 6
    
    print(currentpos)
    print(flags)
print("lastpos " + str(currentpos)+ " flags "+str(flags))
signal.signal(signal.SIGINT, handler)

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")
print("Calibration current is " + str(my_drive.axis0.motor.config.calibration_current) + "A")

# Set some hardware parameters temporarily
print("setting some hardware parameters temporarily")
my_drive.config.brake_resistance = 0.5
my_drive.axis0.motor.config.pole_pairs = 7

# Calibrate
print("starting calibration")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

print("waiting for calibration to end...")
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

# Closed loop control 
print("Changing state to closed loop control")
#my_drive.axis0.config.sensorless_ramp.vel = 380.95/60 * 2 * math.pi * 7
my_drive.axis0.config.sensorless_ramp.vel = 300/60 * 2 * math.pi * 7
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

while my_drive.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
    print("axis errors are:")
    print(hex(my_drive.axis0.error))	
    print("motor errors are:")
    print(hex(my_drive.axis0.motor.error))
    print("encoder errors are:")
    print(hex(my_drive.axis0.encoder.error))
    time.sleep(0.1)

print("current state is " + str(my_drive.axis0.current_state))

p = subprocess.Popen(["./HolofanRenderer/main_ser"])

time.sleep(1000)
