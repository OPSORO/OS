

import threading
import time
import numpy as np
from opsoro.console_msg import *





class CManager():
    """
        this is a managing class for the camera systems. The manager
        executes the systems in a separate thread. The thread can be
        started and stopped. When there are no systems to execute the
        manager is turned of. The moment were systems been added the
        manager automatically starts
    """
    def __init__(self,videoCapture, *args,**kwargs):
        self.cap = videoCapture
        self.csystems = []
        self.refresh_rate = 0
        self._stop_event = threading.Event()
        self._start_event = threading.Event()
        self.thread = None

    def setCap(self,cap):
        self.cap = cap

    def run(self):
        while(not self._stop_event.is_set()):
            begintime = time.time()
            csystems_copy = list(self.csystems)
            ret, frame = self.cap.read()
            if ret:
                for s in csystems_copy:
                    s.update(frame)
                    if self._stop_event.is_set():
                        break
            else:
                print_warning("Camera Error")
            self.refresh_rate = 1/(time.time() - begintime)

    def stop(self):
        self._stop_event.set()
        self._start_event.clear()
        self.thread = None


    def start(self):
        self._start_event.set()
        self._stop_event.clear()
        if self.csystems is not None and len(self.csystems)>0 and self.cap is not None:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()


    def addSystem(self, system):
        if self.getSystem(system.__class__) is None:
            self.csystems += [system]
        if self._start_event.is_set():
            self.start()


    def removeSystem(self, system_class):
        newSystemList = []
        for s in list(self.csystems):
            print not isinstance(s,system_class)
            if not isinstance(s,system_class):
                newSystemList += [s]
        self.csystems = newSystemList


    def getSystem(self,system_class):
        for s in self.csystems:
            if isinstance(s,system_class):
                return s
        return None

    def removeAllSystems(self):
        self.csystems = []
        self._stop_event.set()
