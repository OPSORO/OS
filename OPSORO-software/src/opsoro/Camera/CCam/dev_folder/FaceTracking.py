import cv2
import cv2.cv as cv
import numpy as np
from Camera import CCam

PATH_HAAR_CASCADE = 'haarcascade_frontalface_default1.xml'
faceCascade = cv2.CascadeClassifier(PATH_HAAR_CASCADE)
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)


class FaceTracking():
    def __init__(self):
        self.selection = None
        self.refHist = None
        self.previousHist = None
        self.previousFrame = None

    def update(self,frame):
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv,5)
        if self.selection is None: #viola Jones
            face = self.faceDetect(frame)
            if face is not None:
                self.selection = face
        else: # CamShift
            backProj = cv2.calcBackProject([hsv], [0], self.previousHist, [0, 255], 1)
            r, self.selection = cv2.CamShift(backProj, tuple(self.selection), termination)
            vis= frame.copy()
            vis[:] = backProj[..., np.newaxis]
            cv2.imshow('backProj',vis)

        if self.selection is not None:
            hist = self.calHist(hsv,self.selection)
            if self.previousHist is None or self.refHist is None:
                self.previousHist = hist
                self.refHist = hist
            else:
                self.previousHist = 0.4 * self.refHist + 0.4 * self.previousHist + 0.2 * hist

            self.show_hist(self.previousHist)
            if cv2.compareHist(hist,self.refHist,cv2.cv.CV_COMP_INTERSECT) <50:
                self.selection = None
                print "I'm lost"





    def show_hist(self,hist):
        bin_count = hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)



    def calHist(self, hsv,selection):
        x,y,w,h = selection
        mask = np.zeros_like(hsv[:,:,0])
        cv2.ellipse(mask, center=(x+w/2, y+h/2), axes=(w/4, h/4), angle=0, startAngle=0, endAngle=360,color=(255, 255, 255), thickness=-1)#een cirkel als masker om zo veel mogelijk van de achtergrond weg te filteren
        cv2.imshow('mask', mask)
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
        return self.selection

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    tracker = FaceTracking()
    while (True):
        ret, frame = cap.read()
        # frame = cv2.medianBlur(frame, 9)
        tracker.update(frame)
        face = tracker.getFacePos()
        if face is not None:
            x, y, w, h = face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.imshow('frame', frame)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        hsv = cv2.medianBlur(hsv,5)
        h = hsv.copy(); hsv[:, :, 1] = 0; hsv[:, :, 2] = 0;
        # s = hsv.copy(); hsv[:, :, 0] = 0; hsv[:, :, 2] = 0;
        # v = hsv.copy(); hsv[:, :, 0] = 0; hsv[:, :, 1] = 0;
        cv2.imshow('h',h)
        # cv2.imshow('s', s)
        # cv2.imshow('v', v)
        if cv2.waitKey(1) & 0xFF == 27:
            break