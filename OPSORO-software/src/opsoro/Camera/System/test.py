import cv2
#from  opsoro.Camera import Camera

PATH_HAAR_CASCADE = 'haarcascade_frontalface_default.xm'
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)




class FaceTracking():
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier(PATH_HAAR_CASCADE)
        print self.faceCascade
        self.faceRectangle = None  # (x,y,w,h)
        self.selection = None
        self.previousHist = None
        self.previousFrame = None

    def update(self,frame):
        #frame = Camera.getFrame()
        if self.selection is None:  # viola Jones
            face = self.faceDetect(frame)
            if face is not None:
                self.selection = face
        else:  # CamShift
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            backProj = cv2.calcBackProject([hsv], [0], self.previousHist, [0, 255], 1)
            (r, newSelection) = cv2.CamShift(backProj, self.selection, termination)
            print newSelection
            hist = self.calHist(frame, self.selection)

    def calHist(frame, selection):
        roi = frame[roiPts[1]:roiPts[-1], roiPts[0]:roiPts[2]]
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
        frame.shape[0], frame.shape[1]))  # een cirkel als masker om zo veel mogelijk van de achtergrond weg te filteren
        hist = cv2.calcHist([roi], [0], mask, [16], [0, 255])
        hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        return hist

    def faceDetect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        face = None
        if len(faces) == 1:
            face = faces[0]
        elif len(faces) > 1:
            face = max([(w * h, (x, y, w, h)) for x, y, w, h in faces], key=lambda i: i[0])[1]
        return face




if __name__ == '__main__':
    f = FaceTracking()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if f.selection:
            x,y,w,h = f.selection
            cv2.rectangle(frame,(x,y),(x+w,y+h),255,3)
        cv2.imshow('main',frame)

        f.update(frame)

        k = 0xFF & cv2.waitKey(1)
        if k == ord('q'):
            break;
