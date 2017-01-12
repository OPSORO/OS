import cv2
import os
import os.path
import subprocess, signal
import threading

from opsoro.console_msg import *

from opsoro.Camera.CCam.CManager import CManager
from opsoro.Camera.CCam.FaceTracking_MeanShift import FaceTracking

C_SYSTEMS = {'FaceTracking':FaceTracking}


class _Camera(object):
    def __init__(self):
        self.cap = None
        self.resolution = None
        self.c_manager = CManager(None)


    def startInternetStream(self):
        """
            start the motion server on port 8080
            edit configs: /etc/motion/motion.conf
            motion server can't be combined with the opencv alghoritms
        """
        devnull = open('/dev/null', 'w')
        proc = subprocess.Popen(["motion"], stdout=subprocess.PIPE, stderr=devnull)
        print_info("Motion server on")

    def stopInternetStream(self):
        """
            Stops motion server
        """
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
        """
            starts the opencv video capture, when there are CSystems available, they will be executed by the CManager
        """
        self.cap = cv2.VideoCapture(0)
        while not self.cap.isOpened():
            pass
        self.resolution = (self.cap.get(3),self.cap.get(4))
        self.c_manager.setCap(self.cap)
        self.c_manager.start()

    def stopSystemProcessing(self):
        """
        CManager stops, opencv videoCapture released
        """
        self.c_manager.stop()
        self.cap.release()

    def registerSystem(self,system_class,*args,**kwargs):
        """
        Adds a CSystem to the CManager, when the manager is running the system will be executed emidiatly.

        :params string system_class         Name of the CSystem-class defined C_SYSTEMS
        :params *args,**kwargs              extra arguments required  by the CSystem constructor
        """
        if system_class in C_SYSTEMS:
            s = C_SYSTEMS[system_class](*args,**kwargs)
            self.c_manager.addSystem(s)
            print_info(str(s) + " is added to Camera Manager")

    def unregisterSystem(self,system_class):
        """
        Removes a CSystem from the CManager.

        :param string system_class      Name of the CSystem-class defined C_SYSTEMS
        """
        if system_class in C_SYSTEMS:
            self.c_manager.removeSystem(C_SYSTEMS[system_class].__class__)

    def unregisterAllSystem(self):
        """
        Removes all CSystems from the CManager.
        """
        self.c_manager.removeAllSystems()


    def getFaceCenter(self):
        """
        returns the latest updated center position of the face

        :return     dof value, tuple with pare of float values between [-1,1]
        """
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
        """
        returns the latest updated position of the uper-left and
        bottom-right corner ot the face rectangle

        :return     tuple of pionts, a point is a tuple with pare of float values between [-1,1]
        """
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
        """
        returns the refresh-rate of the CManager.

        :return          refresh-rate, loops per second
        :rtype:          float
        """
        return self.c_manager.refresh_rate

Camera = _Camera()
