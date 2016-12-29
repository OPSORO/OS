import cv2
import numpy as np
import os
from opsoro.Camera.CCam.CSystem import CSystem



PATH_HAAR_CASCADE = os.path.dirname(__file__) +'/extra/haarcascade_frontalface_default1.xml'
faceCascade = cv2.CascadeClassifier(PATH_HAAR_CASCADE)
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)


class FaceTracking(CSystem):
    def __init__(self):
        self.facePosition = None
        self.selection = None
        self.refHist = None
        self.previousHist = None

    def update(self,frame):
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv,5)
        if self.selection is not None and self.previousHist is not None and self.refHist is not None: #CamShift
            print "CamShift"
            backProj = cv2.calcBackProject([hsv], [0], self.previousHist, [0, 255], 1)
            r, self.selection = cv2.CamShift(backProj, tuple(self.selection), termination)

            hist = self.calHist(hsv, self.selection)
            if cv2.compareHist(hist,self.refHist,cv2.cv.CV_COMP_INTERSECT) < 50:
                self.selection = None
            else:
                self.previousHist = 0.4 * self.refHist + 0.4 * self.previousHist + 0.2 * hist

        if self.selection is None: #Viola Jones
            print "Viola Jones"
            face = self.faceDetect(frame)
            if face is not None:
                self.selection = face
                hist = self.calHist(hsv, self.selection)
                self.previousHist = hist
                self.refHist = hist
            else:
                print "no faces detect"
                self.selection = None
                self.previousHist = None
                self.refHist = None

        self.facePosition = self.selection
        print self.facePosition

    def calHist(self, hsv,selection):
        x,y,w,h = selection
        mask = np.zeros_like(hsv[:,:,0])
        cv2.ellipse(mask, center=(x+w/2, y+h/2), axes=(w/4, h/4), angle=0, startAngle=0, endAngle=360,color=(255, 255, 255), thickness=-1)#een cirkel als masker om zo veel mogelijk van de achtergrond weg te filteren
        hist = cv2.calcHist([hsv], [0], mask=mask, histSize = [32], ranges=[0, 255])
        hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        hist = hist.reshape(-1)
        return hist

    def faceDetect(self,frame):
        gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )
        face = None
        if len(faces)==1:
            face= faces[0]
        elif len(faces) > 1:
            face = max([(w*h,(x,y,w,h)) for x,y,w,h in faces], key=lambda i:i[0])[1]
            face = face
        return face

    def getFacePos(self):
        return self.facePosition

    def __str__(self):
        return "FaceTracking"

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    print (cap.get(3),cap.get(4))
    tracker = FaceTracking()
    while (True):
        ret, frame = cap.read()
        tracker.update(frame)
        face = tracker.getFacePos()
        if face is not None:
            x, y, w, h = face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv, 5)
        h = hsv.copy(); hsv[:, :, 1] = 0; hsv[:, :, 2] = 0;
        cv2.imshow('h',h)
        if cv2.waitKey(1) & 0xFF == 27:
            print face
            break
