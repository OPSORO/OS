import cv2
import os
import os.path
import subprocess, signal
import threading

from opsoro.console_msg import *

from opsoro.Camera.CCam.CManager import CManager
from opsoro.Camera.CCam.FaceTracking import FaceTracking

C_SYSTEMS = {'FaceTracking':FaceTracking}


class _Camera(object):
    def __init__(self):
        self.cap = None
        self.resolution = (0,0)
        self.c_manager = CManager(None)


    def startInternetStream(self):
        devnull = open('/dev/null', 'w')
        proc = subprocess.Popen(["motion"], stdout=subprocess.PIPE, stderr=devnull)
        print_info("Motion server on")

    def stopInternetStream(self):
        proc = subprocess.Popen(["pgrep", "motion"], stdout=subprocess.PIPE)

        # Kill process.
        for pid in proc.stdout:
            os.kill(int(pid), signal.SIGTERM)
            # Check if the process that we killed is alive.
            if os.path.exists("/proc/" + str(pid)):
                print_info("Wasn't able to kill the motion process. HINT:use signal.SIGKILL or signal.SIGABORT")
            else:
                print_info("Motion server off")

    def startSystemProcessing(self):
        self.cap = cv2.VideoCapture(0)
        while not self.cap.isOpened():
            pass
        self.resolution = (self.cap.get(3),self.cap.get(4))
        self.c_manager.setCap(self.cap)
        self.c_manager.start()

    def stopSystemProcessing(self):
        self.c_manager.stop()
        self.cap.release()

    def registerSystem(self,system_class,*args,**kwargs):
        if system_class in C_SYSTEMS:
            s = C_SYSTEMS[system_class](*args,**kwargs)
            self.c_manager.addSystem(s)
            print_info(str(s) + " is added to Camera Manager")

    def unregisterSystem(self,system_class):
        if system_class in C_SYSTEMS:
            self.c_manager.removeSystem(C_SYSTEMS[system_class].__class__)

    def unregisterAllSystem(self):
        self.c_manager.removeAllSystems()


    def getFaceCenter(self):
        global C_SYSTEMS
        sys = self.c_manager.getSystem(C_SYSTEMS['FaceTracking'])
        if sys is not None:
            pos = sys.getFacePos()
            if pos is not None:
                x, y, w, h = pos
                center = [((x+0.5 * w) * 2 - self.resolution[0]) / self.resolution[0],
                          ((y+0.5 * h) * 2 - self.resolution[1]) / self.resolution[1]]
                return center
        return None

    def getFaceCorners(self):
        sys = self.c_manager.getSystem(C_SYSTEMS['FaceTracking'])
        if sys is not None:
            pos = sys.getFacePos()
            if pos is not None:
                x, y, w, h = pos
                top_left = [float(x * 2 - self.resolution[0]) / self.resolution[0],
                          float(y * 2 - self.resolution[1]) / self.resolution[1]]
                bottom_right = [float((x+w) * 2 - self.resolution[0]) / self.resolution[0],
                            float((y+h) * 2 - self.resolution[1]) / self.resolution[1]]
                return [top_left,bottom_right ]
        return None

    def getRefreshRate(self):
        return self.c_manager.refresh_rate
Camera = _Camera()
