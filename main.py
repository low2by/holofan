from FaceDetector import FaceDetector
from Stepper import Stepper
from ObjectSpace import ObjectSpace


def search(detector, stepper, space):
    global last_step_dir
    
    while True:
        faces = detector.detect()

        if len(faces)==0:
            stepper.step_num(1, last_step_dir)
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

stepper = Stepper()
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
        centery = int(faces[0][1] + faces[0][3]/2)
        if centerx < w/2 - w*0.05:
            print("step_left")
            last_step_dir = 'forward'
            stepper.step_num(4, 'forward')
            space.rotateModel(-1.8)
            space.update()
        elif centerx > w/2 + w*0.05:
            print("step_right")
            last_step_dir = 'backward'
            stepper.step_num(4, 'backward')
            space.rotateModel(1.8)
            space.update()
        
        if centery < h/2 - h*0.05:
            print("image_down")
            #last_step_dir = 'forward'
            #stepper.step_num(4, 'forward')
            space.rotateModel(-1.8, 'z')
            space.update()
        elif centery > h/2 + h*0.05:
            print("image_up")
            #last_step_dir = 'backward'
            #stepper.step_num(4, 'backward')
            space.rotateModel(1.8, 'z')
            space.update()        
        else:
            print("stay")
    else:
        no_face_found_count += 1
        if(no_face_found_count > 10):
            search(detector, stepper, space)

    detector.output(faces)            
