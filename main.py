from FaceDetector import FaceDetector
from Stepper import Stepper
from ObjectSpace import ObjectSpace

space = ObjectSpace()
space.load_obj("banana.obj", "banana")
space.update()

stepper = Stepper()
detector = FaceDetector()
w, h = detector.useCam()
print(w/2 - w*0.05, w/2 + w*0.05)
itr = 0
while True:
    faces = detector.detect()

    if len(faces)>0:
        centerx = int(faces[0][0] + faces[0][2]/2)
        if centerx < w/2 - w*0.05:
            print("step_left")
            stepper.step_num(4, 'forward')
            space.rotateModel(-1.8)
            space.update()
        elif centerx > w/2 + w*0.05:
            print("step_right")
            stepper.step_num(4, 'backward')
            space.rotateModel(1.8)
            space.update()
        else:
            print("stay")

    detector.output(faces)
