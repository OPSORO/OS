from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
#from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
from hardware import Hardware
import argparse
import imutils
import time
import cv2
import numpy as np
from collections import deque
import threading
import sys
#alles in 1 doorlopende functie :)
class _Detection(object):
    vs = None
    def start_stream(self):
        try:
            global vs
            PiCamera.vflip = False
            vs = PiVideoStream().start()
            time.sleep(1)
            return vs
        except Exception as e:
            return None

    def stop_stream(self):
        global vs
        vs.stop()

    def is_color_detected(self,color):
        try:
            global vs
            def check_for_color(vs):
                frame = vs.read()
                frame = imutils.resize(frame, width=400)
                if args["display"] > 0:
                    blurred = cv2.GaussianBlur(frame, (11,11),0)
                    mask = cv2.inRange(frame, colorLower, colorUpper)
                    mask = cv2.erode(mask, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                    if len(cnts) > 0:
                        return True
                    else:
                        return False
            ap = argparse.ArgumentParser()
            ap.add_argument("-d", "--display", type=int, default=1, help="Wheter or not frames should be displayed")
            ap.add_argument("-b", "--buffer", type=int, default=2500, help="Max buffer size")
            args = vars(ap.parse_args())
            if color == "#ff0000":
                colorLower = np.array([145, 69, 20])
                colorUpper = np.array([192, 255,255])
            if color == "#00ff00":
                colorLower = np.array([29, 86, 20])
                colorUpper = np.array([64, 255,255])
            if color == "#0000ff":
                colorLower = np.array([100, 86, 20])
                colorUpper = np.array([130, 255,255])
            if color == "#ffff00":
                colorLower = np.array([20, 86, 20])
                colorUpper = np.array([40, 255,255])

            pts = deque(maxlen=args["buffer"])
            return check_for_color(vs)
        except Exception as e:
            return None


    def get_color_coords(self, color):
        global vs
        def check_for_color_coords(vs):
            arrCoords = [175,175]
            frame = vs.read()
            frame = imutils.resize(frame, width=350)
            if args["display"] > 0:
                blurred = cv2.GaussianBlur(frame, (11,11),0)
                mask = cv2.inRange(frame, colorLower, colorUpper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                if len(cnts) > 0:
                    c = max(cnts, key=cv2.contourArea)
                    ((x,y),radius) = cv2.minEnclosingCircle(c)
                    if radius > 0:
                        arrCoords[0] = x
                        arrCoords[1] = y
                        return arrCoords
                    else:
                        return arrCoords
                else:
                    return arrCoords
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--display", type=int, default=1, help="Wheter or not frames should be displayed")
        ap.add_argument("-b", "--buffer", type=int, default=2500, help="Max buffer size")
        args = vars(ap.parse_args())
        if color == "#ff0000":
            colorLower = np.array([145, 69, 20])
            colorUpper = np.array([192, 255,255])
        if color == "#00ff00":
            colorLower = np.array([29, 86, 20])
            colorUpper = np.array([64, 255,255])
        if color == "#0000ff":
            colorLower = np.array([100, 86, 20])
            colorUpper = np.array([130, 255,255])
        if color == "#ffff00":
            colorLower = np.array([20, 86, 20])
            colorUpper = np.array([40, 255,255])
        pts = deque(maxlen=args["buffer"])
        arrCoords = check_for_color_coords(vs)
        return arrCoords

    def get_color_coord_x(self, color):
        global vs
        def check_for_color_coord_x(vs):
            frame = vs.read()
            frame = imutils.resize(frame, width=350)
            if args["display"] > 0:
                blurred = cv2.GaussianBlur(frame, (11,11),0)
                mask = cv2.inRange(frame, colorLower, colorUpper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                if len(cnts) > 0:
                    c = max(cnts, key=cv2.contourArea)
                    ((x,y),radius) = cv2.minEnclosingCircle(c)
                    if radius > 0:
                        return x
                    else:
                        return 175
                else:
                    return 175
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--display", type=int, default=1, help="Wheter or not frames should be displayed")
        ap.add_argument("-b", "--buffer", type=int, default=2500, help="Max buffer size")
        args = vars(ap.parse_args())
        if color == "#ff0000":
            colorLower = np.array([145, 69, 20])
            colorUpper = np.array([192, 255,255])
        if color == "#00ff00":
            colorLower = np.array([29, 86, 20])
            colorUpper = np.array([64, 255,255])
        if color == "#0000ff":
            colorLower = np.array([100, 86, 20])
            colorUpper = np.array([130, 255,255])
        if color == "#ffff00":
            colorLower = np.array([20, 86, 20])
            colorUpper = np.array([40, 255,255])
        pts = deque(maxlen=args["buffer"])
        x = check_for_color_coord_x(vs)
        return x

    def get_color_coord_y(self, color):
        global vs
        def check_for_color_coord_y(vs):
            frame = vs.read()
            frame = imutils.resize(frame, width=350)
            if args["display"] > 0:
                blurred = cv2.GaussianBlur(frame, (11,11),0)
                mask = cv2.inRange(frame, colorLower, colorUpper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                if len(cnts) > 0:
                    c = max(cnts, key=cv2.contourArea)
                    ((x,y),radius) = cv2.minEnclosingCircle(c)
                    if radius > 0:
                        return y
                    else:
                        return 175
                else:
                    return 175
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--display", type=int, default=1, help="Wheter or not frames should be displayed")
        ap.add_argument("-b", "--buffer", type=int, default=2500, help="Max buffer size")
        args = vars(ap.parse_args())
        if color == "#ff0000":
            colorLower = np.array([145, 69, 20])
            colorUpper = np.array([192, 255,255])
        if color == "#00ff00":
            colorLower = np.array([29, 86, 20])
            colorUpper = np.array([64, 255,255])
        if color == "#0000ff":
            colorLower = np.array([100, 86, 20])
            colorUpper = np.array([130, 255,255])
        if color == "#ffff00":
            colorLower = np.array([20, 86, 20])
            colorUpper = np.array([40, 255,255])
        pts = deque(maxlen=args["buffer"])
        y = check_for_color_coord_y(vs)
        return y

    def get_face_coords(self):
        arrCoords = [175,175]
        face = cv2.CascadeClassifier('data/visprog/scripts/haarcascade_frontalface_default')
        frame = vs.read()
        frame = imutils.resize(frame, width=350)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        facedet = face.detectMultiScale(gray, 1.3,5)
        if facedet != ():
            for(x,y,w,h) in facedet:
                arrCoords[0] = x + (w/2)
                arrCoords[1] = y + (h/2)
                return arrCoords
        else:
            return arrCoords

    def get_face_coord_x(self):
        face = cv2.CascadeClassifier('data/visprog/scripts/haarcascade_frontalface_default')
        frame = vs.read()
        frame = imutils.resize(frame, width=350)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        facedet = face.detectMultiScale(gray, 1.3,5)
        if facedet != ():
            for(x,y,w,h) in facedet:
                xValue = x + (w/2)
                return xValue
        else:
            xValue = 175
            return xValue

    def get_face_coord_y(self):
        face = cv2.CascadeClassifier('data/visprog/scripts/haarcascade_frontalface_default')
        frame = vs.read()
        frame = imutils.resize(frame, width=350)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        facedet = face.detectMultiScale(gray, 1.3,5)
        if facedet !=():
            for(x,y,w,h) in facedet:
                yValue = y + (h/2)
                return yValue
        else:
            yValue = 175
            return yValue


    def initialize_predictor(self):
        global predictor
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


    def receive_face_points(self, numberLandmark):
        global vs
        global predictor
        def get_landmarks(im):
            rects = cascade.detectMultiScale(im, 1.3,5)
            x,y,w,h = rects[0]
            if len(rects) >= 1:
                rect=dlib.rectangle(int(x),int(y),int(x+w),int(y+h))
                return np.matrix([[p.x,p.y] for p in predictor(im, rect).parts()])

        def annotate_landmarks(im, landmarks, numberLandmark):
            arrCoords = [175,175]
            for idx, point in enumerate(landmarks):
                pos = (point[0, 0], point[0, 1])
                if idx == numberLandmark:
                    arrCoords[0] = landmarks[numberLandmark,0]
                    arrCoords[1] = landmarks[numberLandmark,1]
            return arrCoords
        frame = vs.read()
        cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        frame = imutils.resize(frame, width=350)
        blurred = cv2.GaussianBlur(frame, (11,11),0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        try:
            landmarks = get_landmarks(frame)
            arrCoords = annotate_landmarks(frame, landmarks, numberLandmark)
            return arrCoords

        except:
            return [175,175]


    def follow_object(self,xCoord,yCoord):
        rechter_x = 1350 + (xCoord * 2)
        rechter_y = 1875 - (yCoord * 2)

        linker_x = 1200 + (xCoord * 2)
        linker_y = 1175 + (yCoord * 2)

        Hardware.servo_set(3,int(rechter_x))
        Hardware.servo_set(2,int(rechter_y))

        Hardware.servo_set(13, int(linker_x))
        Hardware.servo_set(12, int(linker_y))

		#reghter oog horizontaal
		#Hardware.servo_set(3,1350)
		#reghter oog verticaal
		#Hardware.servo_set(2,reghtery)
		#linker oog horizontaal
		#Hardware.servo_set(13,1900)
		#linker ook vertikaal
		#Hardware.servo_set(12,1525)
		#rechter oog:
		#horizontaal = 3
		#mid: 1700
	    #min: -350
	    #max: +350
		#verticaal = 2
		#mid: 1525
		#min: +350
		#max: -350
		#kniperen = 4
		#mid: 1500
	    #min: +300
	    #max: -350
		#
		#linker oog :
		#horizontaal = 13
		#mid: 1550
	  	#min: -350
	  	#max: +350
		#vertikaal = 12
		#mid: 1525
	    #min: -350
	    #max: +350
		#kniperen = 11
		#mid: 1525
	    #min: -300
	    #max: +350
		#
		#rezolutie width =350 hieght = 350



Detection = _Detection()
