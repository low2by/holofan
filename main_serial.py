from FaceDetector import FaceDetector
from Stepper import Stepper
import math 
import subprocess
import odrive
from odrive.enums import *
import time
import signal
import sys
import serial
import struct

ser = serial.Serial ("/dev/ttyS0")    #Open named port 
ser.baudrate = 9600                     #Set baud rate to 9600
    
def handler(signum, frame):
    ser.close()
    my_drive.axis0.config.sensorless_ramp.vel = 0
    my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    exit(1)

horizontal_angle = 45;
vertical_angle = -90;

def search(detector, stepper):
    global last_step_dir
    global horizontal_angle
    global ser
    global verticle_angle

    while True:
        faces = detector.detect()

        if len(faces)==0:
            stepper.step(last_step_dir)
            if last_step_dir == 'forward':
                horizontal_angle -= 1.8
                # space.rotateModel(-1.8)
                # space.update()
            else:
                horizontal_angle += 1.8
                # space.rotateModel(1.8)
                # space.update()
                                
            horizontal_angle_bytes = bytearray(struct.pack("f", horizontal_angle))
            vertical_angle_bytes = bytearray(struct.pack("f", vertical_angle))
            
            data_bytes = horizontal_angle_bytes + vertical_angle_bytes
            
            print(str(vertical_angle) + " | " + str(horizontal_angle))
            for byte in data_bytes:
                print(hex(byte))
    
            print("\n\n")
            ser.write(data_bytes)                         #Send back the received data
            # p.stdin.write(bytes(str(horizontal_angle)+"|"+str(vertical_angle)+"\n", "ascii"))
            # p.stdin.flush()
            #print(stdout_data)
        else:
            return faces
            
def imagetransform(yaxis, height, bcam = 5, bobj = 6, hdiff = 0.8333):
    #equation 1
    camangle = -((yaxis/float(height))*90-45)
    #print('...............')
    #print(camangle)
    acam=math.sqrt(math.pow((bcam/math.cos(math.radians(camangle))), 2) - math.pow(bcam,2))
    acam = -acam if camangle < 0 else acam
    #print(acam)
    aobj = acam+hdiff
    #print(aobj)
    objangle=-math.asin((aobj/math.sqrt(math.pow(aobj,2) + math.pow(bobj, 2))))
    #print(objangle)
    #rint('...............')
    return math.degrees(objangle)

if(len(sys.argv) > 1 and sys.argv[1] == "spin"):
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

stepper = Stepper()
detector = FaceDetector()
w, h = detector.useCam()
last_step_dir = 'backward'
#print(w/2 - w*0.05, w/2 + w*0.05)
itr = 0
no_face_found_count = 0;
p = subprocess.Popen(["./HolofanRenderer/main_comm"], stdin=subprocess.PIPE)
while True:
    faces = detector.detect()

    if len(faces)>0:
        no_face_found_count = 0
        centerx = int(faces[0][0] + faces[0][2]/2)
        centery = int(faces[0][1] + faces[0][3]/2)
        if centerx < w/2 - w*0.05:
            #print("step_left")
            last_step_dir = 'forward'
            stepper.step('forward')
            horizontal_angle -= 1.8
            # space.rotateModel(-1.8)
            # space.update()
        elif centerx > w/2 + w*0.05:
            #print("step_right")
            last_step_dir = 'backward'
            stepper.step('backward')
            horizontal_angle += 1.8
            # space.rotateModel(1.8)
            # space.update()
        
        # if centery:
            # print("image_down")
            #last_step_dir = 'forward'
            #stepper.step_num(4, 'forward')
        vertical_angle = imagetransform(centery, h) #hoping it is in the z direction
        # elif centery > h/2 + h*0.05:
            # print("image_up")
            # #last_step_dir = 'backward'
            # #stepper.step_num(4, 'backward')
            # space.rotateModel(1.8, 'x')
            # space.update()        
        # else:
            # print("stay")
    else:
        no_face_found_count += 1
        if(no_face_found_count > 10):
            search(detector, stepper)
    
    horizontal_angle_bytes = bytearray(struct.pack("f", horizontal_angle))
    vertical_angle_bytes = bytearray(struct.pack("f", vertical_angle))
    
    data_bytes = horizontal_angle_bytes + vertical_angle_bytes
    
    for byte in data_bytes:
        print(byte)
    
    print("\n\n")
    ser.write(data_bytes)             
    # p.stdin.write(bytes(str(horizontal_angle)+"|"+str(vertical_angle)+"\n", "ascii"))
    # p.stdin.flush()
    #print(stdout_data)

    detector.output(faces)            

