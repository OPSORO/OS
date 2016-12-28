import cv2

class CVCamera(opject):
    def __init__(self):
        self.cap = VideoCapture(0)


    def getFrame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            return None

    def getFacePosition(self):
