import cv2
import numpy as np
import os



PATH_HAAR_CASCADE = os.path.dirname(__file__) +'/extra/haarcascade_frontalface_default1.xml'
faceCascade = cv2.CascadeClassifier(PATH_HAAR_CASCADE)
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10, 1)
REDETECT_FACE = 10 #maximum amount os mean-shift search operations

class Counter():
    def __init__(self,size):
        self.size = size
        self.count_val = 0
    def check(self):
        if self.count_val == self.size:
            self.count_val = 0
            return True
        else:
            self.count_val += 1
            return False


class FaceTracking():
        """
            face detection and tracking algorithm.
                1. detect face with Viole Jones face detection algorithm
                2. folows the face using Mean-Shift color tracking
        """
    def __init__(self):
        self.facePosition = None
        self.state = 0          #    0=Viola Jones   1=CamShift
        self.selection = None #selection rectangle
        self.face_refresh_counter = Counter(REDETECT_FACE)
        self.refHist = None
        self.ref_selection = None
        self.previousHist = None

    def update(self,frame):
        frame[:, :, 0] = cv2.equalizeHist(frame[:, :, 0])
        frame[:, :, 1] = cv2.equalizeHist(frame[:, :, 1])
        frame[:, :, 2] = cv2.equalizeHist(frame[:, :, 2])
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        # hsv = cv2.medianBlur(hsv,5)

        new_selection = None


        if self.face_refresh_counter.check():
            self.state = 0

        if self.state == 1: #Mean-Shift
            print "Mean-Shift"
            backProj = cv2.calcBackProject([hsv], [0], self.previousHist, [0, 255], 1)
            backProj &= self.backgroundMask(hsv)
            # cv2.imshow("back proj",backProj)

            ret ,new_selection = cv2.meanShift(backProj, tuple(self.selection), termination)

            hist = self.calHist(hsv, new_selection)
            if cv2.compareHist(hist,self.refHist,cv2.cv.CV_COMP_INTERSECT) < 250:
                self.state = 0
            else:
                # self.show_hist(self.refHist,'res hist')
                # self.show_hist(self.previousHist, 'prev hist')
                # self.show_hist(hist, 'hist')
                self.previousHist = 0.6 * self.refHist  + 0.2 * self.previousHist + 0.2 * hist

        if self.state == 0: #Viola Jones
            print "Viola Jones"
            face = self.faceDetect(frame)
            if face is not None:
                new_selection = face
                hist = self.calHist(hsv, new_selection)
                self.previousHist = hist
                self.refHist = hist
                self.state = 1
            else:
                print "no faces detect"
                new_selection = None
                new_selection_e = None
                self.previousHist = None
                self.refHist = None

        if new_selection is not None and self.selection is not None:
            x1, y1, w1, h1 = self.selection
            x2, y2, w2, h2 = new_selection
            moving_dist = np.sqrt(np.power((x1+0.5*w1)-(x2+0.5*w2),2) + np.power((y1+0.5*y1)-(y2+0.5*y2),2))
            if moving_dist > 100:
                self.state = 0
                new_selection = None
            else:
                self.facePosition = new_selection

        self.selection = new_selection
        self.facePosition = self.selection



    def backgroundMask(self,frame):
        mask = np.zeros_like(frame[:, :, 0])
        if self.selection is not None:
            x,y,w,h = self.selection
            cv2.ellipse(mask, center=(x + w / 2, y + h / 2), axes=(w, h), angle=0, startAngle=0, endAngle=360,
                        color=(255, 255, 255), thickness=-1)
        return mask

    def calHist(self, hsv, selection):
        mask = np.zeros_like(hsv[:, :, 0])
        x,y,w,h = selection
        cv2.ellipse(mask, center=(x+w/2, y+h/2), axes=(w/4, h/4), angle=0, startAngle=0, endAngle=360,color=255, thickness=-1)#een cirkel als masker om zo veel mogelijk van de achtergrond weg te filteren

        # cv2.imshow("mask",mask)
        hist = cv2.calcHist([hsv], [0], mask=mask, histSize = [24], ranges=[0, 255])
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

    def show_hist(self, hist, name = "hist"):
        bin_count = hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count * bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(hist[i])
            cv2.rectangle(img, (i * bin_w + 2, 255), ((i + 1) * bin_w - 2, 255 - h),
                          (int(255 * i / bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow(name, img)

    def getFacePos(self):
        return self.facePosition

    def __str__(self):
        return "FaceTracking"

if __name__ == "__main__":
    cap = cv2.VideoCapture(1)
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
        h = hsv.copy(); hsv[:, :, 1] = 255; hsv[:, :, 2] = 255;
        cv2.imshow('h',h)
        cv2.imshow('h bgr',cv2.cvtColor(h,cv2.COLOR_HSV2BGR))
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            print face
            break
        elif k == ord('x'):
            tracker.selection = None
