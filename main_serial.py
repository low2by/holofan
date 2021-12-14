from FaceDetector import FaceDetector
from Stepper import Stepper
import math 
import subprocess
import time
import signal
import sys
import serial
import struct

ser = serial.Serial ("/dev/ttyS0", 16000)    #Open named port
    
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

