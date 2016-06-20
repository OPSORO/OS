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
import dlib

#Public variables for global usage
arrCoords = [0,0,0,0,0,0,0]
arrPrevCoords = [0,0,0,0,0,0,0]
arrCurrentServoValues = [1625,1625,1550,1525,1550,1525,1600]
arrDefaultServoValues = [1625,1625,1550,1525,1550,1525,1600]
face_points = [17,21,22,26,54,66,60]
face_servos = [1,0,15,14,5,6,7]

#videostream global variable
vs = None
class _Detection(object):
    #START CAMERA STREAMING
    def start_stream(self):
        try:
            #gathering videostream
            global vs
            PiCamera.vflip = False
            #declaring vs as a video stream
            vs = PiVideoStream().start()
            #camera requires some warmup time to start a stream. 1s is minimum time.
            time.sleep(1)
            return vs
        except Exception as e:
            return None
    #STOP CAMERA STREAMING
    def stop_stream(self):
        #gathering videostream
        global vs
        #stop the global videostream
        vs.stop()

    #CHECK IF COLOR IS DETECTED > If structure - true/false
    def is_color_detected(self,color):
        try:
            #gathering videostream
            global vs
            #check which color and get its upper/lower
            if color == "#ff0000":
                colorLower = np.array([145, 69, 20])
                colorUpper = np.array([192, 255,255])
            if color == "#00ff00":
                colorLower = np.array([29, 86, 20])
                colorUpper = np.array([64, 255,255])
            if color == "#0000ff":
                colorLower = np.array([105, 86, 20])
                colorUpper = np.array([130, 255,255])
            if color == "#ffff00":
                colorLower = np.array([20, 86, 20])
                colorUpper = np.array([40, 255,255])
            pts = deque(maxlen=2500)
            frame = vs.read()
            frame = imutils.resize(frame, width=350)
            blurred = cv2.GaussianBlur(frame, (11,11),0)
            mask = cv2.inRange(frame, colorLower, colorUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 1:
                c = max(cnts, key=cv2.contourArea)
                ((x,y),radius) = cv2.minEnclosingCircle(c)
                return True
            else:
                return False
        except Exception as e:
            return "exit"

    #RECEIVE ARRAY OF X , Y COORDINATE OF COLOR FOR LATER PROGRAMMING
    def get_color_coords(self, color):
        try:
            #gathering videostream
            global vs
            if color == "#ff0000":
                colorLower = np.array([145, 69, 20])
                colorUpper = np.array([192, 255,255])
            if color == "#00ff00":
                colorLower = np.array([29, 86, 20])
                colorUpper = np.array([64, 255,255])
            if color == "#0000ff":
                colorLower = np.array([105, 86, 20])
                colorUpper = np.array([130, 255,255])
            if color == "#ffff00":
                colorLower = np.array([20, 86, 20])
                colorUpper = np.array([40, 255,255])
            pts = deque(maxlen=2500)
            arrCoords = [175,175]
            frame = vs.read()
            frame = imutils.resize(frame, width=350)
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
        except Exception as e:
            return "exit"
    #RECEIVE X COORDINATE OF A CERTAIN COLOR
    def get_color_coord_x(self, color):
        #gathering videostream
        global vs
        if color == "#ff0000":
            colorLower = np.array([145, 86, 20])
            colorUpper = np.array([192, 255,255])
        if color == "#00ff00":
            colorLower = np.array([29, 86, 20])
            colorUpper = np.array([64, 255,255])
        if color == "#0000ff":
            colorLower = np.array([105, 86, 20])
            colorUpper = np.array([130, 255,255])
        if color == "#ffff00":
            colorLower = np.array([20, 86, 20])
            colorUpper = np.array([40, 255,255])
        pts = deque(maxlen=2500)
        xValue = 175
        frame = vs.read()
        frame = imutils.resize(frame, width=350)
        blurred = cv2.GaussianBlur(frame, (11,11),0)
        mask = cv2.inRange(frame, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x,y),radius) = cv2.minEnclosingCircle(c)
            if radius > 0:
                xValue = x
        
        return xValue
        

    #RECEIVE Y COORDINATE OF A CERTAIN COLOR
    def get_color_coord_y(self, color):
       #gathering videostream
        global vs
        if color == "#ff0000":
            colorLower = np.array([145, 69, 20])
            colorUpper = np.array([192, 255,255])
        if color == "#00ff00":
            colorLower = np.array([29, 86, 20])
            colorUpper = np.array([64, 255,255])
        if color == "#0000ff":
            colorLower = np.array([105, 86, 20])
            colorUpper = np.array([130, 255,255])
        if color == "#ffff00":
            colorLower = np.array([20, 86, 20])
            colorUpper = np.array([40, 255,255])
        pts = deque(maxlen=2500)
        yValue = 175
        frame = vs.read()
        frame = imutils.resize(frame, width=350)
        blurred = cv2.GaussianBlur(frame, (11,11),0)
        mask = cv2.inRange(frame, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x,y),radius) = cv2.minEnclosingCircle(c)
            if radius > 0:
                yValue = y
        return yValue
        
    #CHECK IF FACE IS DETECTED > If structure - true/false
    def is_face_detected(self):
        
        face = cv2.CascadeClassifier('/home/pi/OnoSW/haarcascade_frontalface_default.xml')
        frame = vs.read()
        frame = imutils.resize(frame, width=350)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        facedet = face.detectMultiScale(gray, 1.3,5)
        if facedet != ():
            for(x,y,w,h) in facedet:
                return True
        else:
            return False


    #RECEIVE ARRAY OF X , Y COORDINATE OF FACE FOR LATER PROGRAMMING
    def get_face_coords(self):
        
        global vs
        arrCoords = [175,175]
        face = cv2.CascadeClassifier('/home/pi/OnoSW/haarcascade_frontalface_default.xml')
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

    #RECEIVE X COORDINATE OF A FACE
    def get_face_coord_x(self):
        #gathering videostream
        global vs
        #loading cascadefile
        face = cv2.CascadeClassifier('/home/pi/OnoSW/haarcascade_frontalface_default.xml')
        #reading frame from stream
        frame = vs.read()
        #resizing frame for performance
        frame = imutils.resize(frame, width=350)
        #converting to gray
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        facedet = face.detectMultiScale(gray, 1.3,5)
        if facedet != ():
            for(x,y,w,h) in facedet:
                xValue = x + (w/2)
                return xValue
        else:
            xValue = 175
            return xValue

    #RECEIVE Y COORDINATE OF A FACE
    def get_face_coord_y(self):
       
        #gathering videostream
        global vs
        face = cv2.CascadeClassifier('/home/pi/OnoSW/haarcascade_frontalface_default.xml')
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

    #LOADING PREDICTOR! THIS MIGHT TAKE A WHILE! FILE OF 100+MB
    def initialize_predictor(self):
        global predictor
        predictor = dlib.shape_predictor("/home/pi/OnoSW/shape_predictor_68_face_landmarks.dat")
        
    #GET REQUEST FOR PREDICTED FACEPOINTS
    def receive_face_points(self, numberLandmark, coord):
        
        #gathering videostream
        global vs
        global predictor
    
        ############################################
        #RECEIVE LANDMARKS WITH ALL COORDS                                         #
        ############################################
        def get_landmarks(im):
            rects = cascade.detectMultiScale(im, 1.3,5)
            x,y,w,h = rects[0]
            if len(rects) >= 1:
                rect=dlib.rectangle(int(x),int(y),int(x+w),int(y+h))
                return np.matrix([[p.x,p.y] for p in predictor(im, rect).parts()])

        ###########################################
        #GET NECESSARY CONTENT FROM LANDMARKS                                 #
        ############################################
        def annotate_landmarks(im, landmarks, numberLandmark, coord):
            value = None
            if coord == "x":
                for idx, point in enumerate(landmarks):
                    pos = (point[0, 0], point[0, 1])
                    if idx == numberLandmark:
                        value = int(landmarks[numberLandmark,0])
            if coord == "y":
                for idx, point in enumerate(landmarks):
                    pos = (point[0, 0], point[0, 1])
                    if idx == numberLandmark:
                        value = int(landmarks[numberLandmark,1])

            return value
        ############################################
        #END OF FUNCTION ANNOTATE LANDMARKS                                      #
        ############################################
        #frame reading
        frame = vs.read()
        #cascade loading
        cascade = cv2.CascadeClassifier("/home/pi/OnoSW/haarcascade_frontalface_default.xml")
        #Resize frame for performance
        frame = imutils.resize(frame, width=350)
        #Special blur for optimal detection
        blurred = cv2.GaussianBlur(frame, (11,11),0)
        #Converting necessary colors
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        try:
            landmarks = get_landmarks(frame)
        except:
            return None
        value = annotate_landmarks(frame, landmarks, numberLandmark, coord)
        return value

    #SET STANDARD VALUES
    def standard_face(self):
        global arrDefaultServoValues
        global face_servos
        i = 0
        for servo in face_servos:
            Hardware.servo_set(servo, int(arrDefaultServoValues[i]))
            i += 1

    #FACE MIRRORING
    def aanpassen_face(self):
        #gathering videostream
        global vs
        global predictor
        global arrCoords
        global arrPrevCoords
        global arrCurrentServoValues
        global arrDefaultServoValues
        global face_points
        global face_servos
        ############################################
        #BEREKENINGEN SERVO POSITIES AAN DE HAND VAN FACEVALUES#
        ############################################
        def servo_calculate_set(arrValues, arrCurrentServoValues):
            if (arrValues[0] < 50) and (arrValues[0] > -50) and (arrValues[0] != 0):
                AmountToChange = arrValues[0] * 8
                arrCurrentServoValues[0] = AmountToChange
                if arrCurrentServoValues[0] > 1825:
                    arrCurrentServoValues[0] = 1825
                if arrCurrentServoValues[0] < 1325:
                    arrCurrentServoValues[0] = 1325
                Hardware.servo_set(face_servos[0], int(arrCurrentServoValues[0]))
            if (arrValues[1] < 50) and (arrValues[1] > -50) and (arrValues[1] != 0):
                AmountToChange = arrValues[1] * 8
                arrCurrentServoValues[1] -= AmountToChange
                if arrCurrentServoValues[1] > 1825:
                    arrCurrentServoValues[1] = 1825
                if arrCurrentServoValues[1] < 1325:
                    arrCurrentServoValues[1] = 1325
                Hardware.servo_set(face_servos[1], int(arrCurrentServoValues[1]))
            if (arrValues[2] < 50) and (arrValues[2] > -50) and (arrValues[2] != 0):
                AmountToChange = arrValues[2] * 8
                arrCurrentServoValues[2] -= AmountToChange
                if arrCurrentServoValues[2] > 1825:
                    arrCurrentServoValues[2] = 1825
                if arrCurrentServoValues[2] < 1325:
                    arrCurrentServoValues[2] = 1325
                Hardware.servo_set(face_servos[2], int(arrCurrentServoValues[2]))
            if (arrValues[3] < 50) and (arrValues[3] > -50) and (arrValues[3] != 0):
                AmountToChange = arrValues[3] * 8
                arrCurrentServoValues[3] += AmountToChange
                if arrCurrentServoValues[3] > 1825:
                    arrCurrentServoValues[3] = 1825
                if arrCurrentServoValues[3] < 1325:
                    arrCurrentServoValues[3] = 1325
                Hardware.servo_set(face_servos[3], int(arrCurrentServoValues[3]))
            if (arrValues[4] < 50) and (arrValues[4] > -50) and (arrValues[4] != 0):
                AmountToChange = arrValues[4] * 8
                arrCurrentServoValues[4] += AmountToChange
                if arrCurrentServoValues[4] > 1950:
                    arrCurrentServoValues[4] = 1950
                if arrCurrentServoValues[4] < 1250:
                    arrCurrentServoValues[4] = 1250
                Hardware.servo_set(face_servos[4], int(arrCurrentServoValues[4]))
            if (arrValues[5] < 50) and (arrValues[5] > -50) and (arrValues[5] != 0):
                AmountToChange = arrValues[5] * 8
                arrCurrentServoValues[5] += AmountToChange
                if arrCurrentServoValues[5] > 1925:
                    arrCurrentServoValues[5] = 1925
                if arrCurrentServoValues[5]< 1275:
                    arrCurrentServoValues[5] = 1275
                Hardware.servo_set(face_servos[5], int(arrCurrentServoValues[5]))
            if (arrValues[6] < 50) and (arrValues[6] > -50) and (arrValues[6] != 0):
                AmountToChange = arrValues[6] * 8
                arrCurrentServoValues[6] -= AmountToChange
                if arrCurrentServoValues[6] > 1900:
                    arrCurrentServoValues[6] = 1900
                if arrCurrentServoValues[6] < 1200:
                    arrCurrentServoValues[6] = 1200
                Hardware.servo_set(face_servos[6], int(arrCurrentServoValues[6]))

        ############################################
        #END FUNCTION SERVO VALUE SET                                                     #
        ############################################

        ############################################
        #START FUNCTION FACE POINTS RECEIVING                                       #
        ############################################
        def receive_face_points(self, numberLandmark, coord, arrNumber, arrCoords):
            global vs
            global predictor
            def get_landmarks(im):
                rects = cascade.detectMultiScale(im, 1.3,5)
            	x,y,w,h = rects[0]
            	if len(rects) >= 1:
                    rect=dlib.rectangle(int(x),int(y),int(x+w),int(y+h))
                    return np.matrix([[p.x,p.y] for p in predictor(im, rect).parts()])

            def annotate_landmarks(im, landmarks, numberLandmark, coord, arrNumber, arrCoords):
            	value = None
            	if coord == "x":
                    for idx, point in enumerate(landmarks):
                        pos = (point[0, 0], point[0, 1])
                        if idx == numberLandmark:
                            arrCoords[arrNumber] = int(landmarks[numberLandmark,0])
            	if coord == "y":
                    for idx, point in enumerate(landmarks):
                        pos = (point[0, 0], point[0, 1])
                        if idx == numberLandmark:
                            arrCoords[arrNumber] = int(landmarks[numberLandmark,1])

            	return arrCoords[arrNumber]

            frame = vs.read()
            cascade = cv2.CascadeClassifier("/home/pi/OnoSW/haarcascade_frontalface_default.xml")
            frame = imutils.resize(frame, width=350)
            blurred = cv2.GaussianBlur(frame, (11,11),0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #try:
            try:
                landmarks = get_landmarks(frame)
            except:
            	return None
            value = annotate_landmarks(frame, landmarks, numberLandmark, coord, arrNumber, arrCoords)
            return value

        ############################################
        #END FUNCTION FACE POINT DETECTION                                            #
        ############################################

        arrCoords = [0,0,0,0,0,0,0]
        #Receiving nosepoint as base for the other facepoints
        nosepoint = receive_face_points(vs,30,"y",0, arrCoords)
        if nosepoint == None:
            nosepoint = 0
        servobasevalue = None
        #Declaration op multiple threads to receive the y values of the facepoints. Multithreaded because it wasn't good
        #at performance.
        t1 = threading.Thread(target=receive_face_points, args=(vs, face_points[0], "y", 0, arrCoords))
        t2 = threading.Thread(target=receive_face_points, args=(vs, face_points[1], "y", 1, arrCoords))
        t3 = threading.Thread(target=receive_face_points, args=(vs, face_points[2], "y", 2, arrCoords))
        t4 = threading.Thread(target=receive_face_points, args=(vs, face_points[3], "y", 3, arrCoords))
        t5 = threading.Thread(target=receive_face_points, args=(vs, face_points[4], "y", 4, arrCoords))
        t6 = threading.Thread(target=receive_face_points, args=(vs, face_points[5], "y", 5, arrCoords))
        t7 = threading.Thread(target=receive_face_points, args=(vs, face_points[6], "y", 6, arrCoords))
        #Start all threads
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        #Continue when all threads are finished
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        #Initialize counter like a real for loop (i = 0; i < ...; i++)
        i = 0
        #Declaration of array to 0. When one value doesn't work, it'll set to 0.

        arrSubstractedCoords = [0,0,0,0,0,0,0]
        #forloop through each facepoint ==> calculate changes with prev coord
        for facepoint in arrCoords:
            if facepoint == None:
                facepoint = 0
            arrSubstractedCoords[i] = abs(arrCoords[i]) - arrPrevCoords[i]
            i += 1
        #copy current coords to previous coords array
        arrPrevCoords = arrCoords
        #set the values of servos and calculate servo height
        servo_calculate_set(arrSubstractedCoords, arrCurrentServoValues)

    #set servo to x and y coordinate. (eye follow)
    def follow_object(self,xCoord,yCoord):
        rechter_x = 1350 + (xCoord * 2)
        rechter_y = 1875 - (yCoord * 2)
        linker_x = 1200 + (xCoord * 2)
        linker_y = 1175 + (yCoord * 2)
        Hardware.servo_set(3,int(rechter_x))
        Hardware.servo_set(2,int(rechter_y))
        Hardware.servo_set(13, int(linker_x))
        Hardware.servo_set(12, int(linker_y))

Detection = _Detection()
