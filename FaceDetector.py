import cv2
import sys

class FaceDetector():

    image = None

    def __init__(self):
        cascPath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(cascPath)  


    def detect(self, imagePath):
        global image
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.3,
            minNeighbors=5,
            minSize=(30,30),
            flags = cv2.CASCADE_SCALE_IMAGE
            )

        print("Found {0} faces!".format(len(faces)))

        return faces

        # Draw a rectangle around the faces
        

    def output(self, faces):
        global image
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite("output.png", image)  
        # cv2.imshow("Faces found", image)
        # cv2.waitKey(0)

if __name__=="__main__":
    detector = FaceDetector()
    faces = detector.detect("yoink.jpg")
    detector.output(faces)

