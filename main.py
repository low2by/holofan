from FaceDetector import FaceDetector
from Stepper import Stepper

stepper = Stepper()
detector = FaceDetector()
w, h = detector.useCam()
print(w/2 - w*0.05, w/2 + w*0.05)
itr = 0
while True:
    faces = detector.detect("yoink.jpg")

    if len(faces)>0:
        centerx = int(faces[0][0] + faces[0][2]/2)
        if centerx < w/2 - w*0.05:
            print("step_left")
            stepper.step('forward')
        elif centerx > w/2 + w*0.05:
            print("step_right")
            stepper.step('backward')
        else:
            print("stay")

    detector.output(faces)
