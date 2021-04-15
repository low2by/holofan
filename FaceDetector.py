from WebcamVideoStream import WebcamVideoStream
import cv2
import sys

class FaceDetector():

    image = None

    def __init__(self):
        cascPath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(cascPath)
        self.usingCam = False
        self.cam = None

    def useCam(self):
        self.usingCam = True
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
        return 640, 480

    def detect(self, imagePath):
        global image

        if self.usingCam:
            _, image = self.cam.read()
        else:
            image = cv2.imread(imagePath)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.3,
            minNeighbors=5,
            minSize=(30,30),
            flags = cv2.CASCADE_SCALE_IMAGE
            )

        # print("Found {0} faces!".format(len(faces)))

        return faces

        # Draw a rectangle around the faces
        

    def output(self, faces, write=False):
        global image
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            centerx = int(x + w/2)
            centery = int(y + h/2)
            cv2.circle(image,(centerx, centery), 5, (0,0,255), -1)
        if write==True:
            cv2.imwrite("output.png", image)
        else:
            cv2.imshow("Faces found", image)
            cv2.waitKey(1)

if __name__=="__main__":
    if len(sys.argv) == 1:
        detector = FaceDetector()
        faces = detector.detect("yoink.jpg")
        detector.output(faces, True)
    elif sys.argv[1] == "-c":
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
                elif centerx > w/2 + w*0.05:
                    print("step_right")
                else:
                    print("stay")

            detector.output(faces)
