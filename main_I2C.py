from FaceDetector import FaceDetector
from ObjectSpace import ObjectSpace
import smbus

def encode_stepper(steps, dir):
    print(int(steps | (dir<<7)))
    return int(steps | (dir<<7))

def search(detector, space):
    global last_step_dir
    
    while True:
        faces = detector.detect()

        if len(faces)==0:
            #stepper.step_num(1, last_step_dir)
            bus.write_byte(address, encode_stepper(1, 1 if last_step_dir == 'forward' else 0))
            if last_step_dir == 'forward':
                space.rotateModel(-1.8/4)
                space.update()
            else:
                space.rotateModel(1.8/4)
                space.update()
        else:
            return faces

space = ObjectSpace()
space.load_obj("banana.obj", "banana")
space.update()

bus = smbus.SMBus(1)
address = 0x69

detector = FaceDetector()
w, h = detector.useCam()
last_step_dir = 'backward'
print(w/2 - w*0.05, w/2 + w*0.05)
itr = 0
no_face_found_count = 0;
while True:
    faces = detector.detect()

    if len(faces)>0:
        no_face_found_count = 0
        centerx = int(faces[0][0] + faces[0][2]/2)
        if centerx < w/2 - w*0.05:
            print("step_left")
            last_step_dir = 'forward'
            #stepper.step_num(4, 'forward')
            bus.write_byte(address, encode_stepper(4, 1))
            space.rotateModel(-1.8)
            space.update()
        elif centerx > w/2 + w*0.05:
            print("step_right")
            last_step_dir = 'backward'
            #stepper.step_num(4, 'backward')
            bus.write_byte(address, encode_stepper(4, 0))
            space.rotateModel(1.8)
            space.update()
        else:
            print("stay")
    else:
        no_face_found_count += 1
        if(no_face_found_count > 10):
            search(detector, space)

    detector.output(faces)            
