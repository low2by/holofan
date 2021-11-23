from FaceDetector import FaceDetector
from Stepper import Stepper
import math 
import subprocess

horizontal_angle = 0;
vertical_angle = -90;

def search(detector, stepper, space):
    global last_step_dir
    
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
            stdout_data = p.communicate(input=[horizontal_angle, vertical_angle])[0]
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
print(w/2 - w*0.05, w/2 + w*0.05)
itr = 0
no_face_found_count = 0;
p = subprocess.Popen(["../holofan_renderer/main_comm"], stdin=subprocess.PIPE)
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
            search(detector, stepper, space)
    p.stdin.write(str(horizontal_angle)+"|"+str(vertical_angle)+"\n")
    p.stdin.flush()
    #print(stdout_data)

    #detector.output(faces)            

