import cv2
import numpy as np
import os
from opsoro.Camera.CCam.CSystem import CSystem



PATH_HAAR_CASCADE = os.path.dirname(__file__) +'/extra/haarcascade_frontalface_default1.xml'
faceCascade = cv2.CascadeClassifier(PATH_HAAR_CASCADE)
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10, 1)
REDETECT_FACE = 20 #maximum amount os Camshift search operations

def drawMatches(img1, kp1, img2, kp2, matches):
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    for mat in matches:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)

    return out

def moveVector(kp1,kp2,matches):
    mVectors = []
    if len(matches)>0:
        for mat in matches:
            img1_idx = mat.queryIdx
            img2_idx = mat.trainIdx
            (x1,y1) = kp1[img1_idx].pt
            (x2,y2) = kp2[img2_idx].pt

            mVectors += [(x2-x1,y2-y1)]
        return np.mean(mVectors,axis=0)
    else:
        return None,None




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


class FaceTracking(CSystem):
        """
            face detection and tracking algorithm.
                1. detect face with Viole Jones face detection algorithm
                2. folows the face using SURF Feature matching
        """
    def __init__(self):
        #general
        self.face_refresh_counter = Counter(REDETECT_FACE)
        self.facePosition = None
        self.state = 0          #    0=Viola Jones   1=CamShift
        self.selection =  None #selection rectangle

        #Viola Jones


        #Surf
        self.surf = cv2.SURF(400)
        # self.ref_img = None
        # self.ref_kp = None
        # self.ref_des = None

        self.prev_img = None
        self.prev_kp = None
        self.prev_des = None
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)



    def update(self,frame):
        if self.face_refresh_counter.check():
            self.state = 0

        new_selection = None

        if self.state == 1: #Surf

            kp1, des1 = self.prev_kp, self.prev_des
            kp2, des2 = self.surf.detectAndCompute(frame, None)
            matches = self.flann.knnMatch(des1, des2, k=2)

            # Apply ratio test
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            vx,vy = moveVector(kp1,kp2,good)

            if self.selection is not None and vx is not None and vy is not None:
                x,y,w,h = self.selection
                new_selection = (int(x+vx),int(y+vy),w,h)



            #to test
            gray1 = cv2.cvtColor(self.prev_img, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("matches",drawMatches(gray1, kp1, gray2, kp2, good))



        if self.state == 0: #Viola Jones
            print "Viola Jones"
            face = self.faceDetect(frame)
            if face is not None:
                new_selection = face
                self.state = 1
            else:
                print "no faces detect"
                new_selection = None




        if new_selection is not None:
            mask = self.create_mask(frame, new_selection)
            cv2.imshow('mask', mask)
            self.prev_kp, self.prev_des = self.surf.detectAndCompute(frame, mask)

        self.prev_img = frame
        self.selection = new_selection



    def create_mask(self,img,selection,scale = 0.33):
        mask = np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)
        x,y,w,h = selection

        cv2.ellipse(mask, center=(x + w / 2, y + h / 2), axes=(int(w *scale),int(h *scale)), angle=0, startAngle=0, endAngle=360,
                    color=255, thickness=-1)
        return mask

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


        cv2.imshow('result',frame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            print face
            break
        elif k == ord('x'):
            tracker.state = 0
