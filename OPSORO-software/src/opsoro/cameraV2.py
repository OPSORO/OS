from opsoro.stoppable_thread import StoppableThread
from opsoro.console_msg import *
import io
import socket
import struct
import time
import picamera

class _Camera(object):

    def __init__(self):
        self.cap = None
        self.resolution = (640,480)
        self._recording = False
        self.thread = None
        self._stream = None
        self._subscribers = []

    def subscribe(self, id):
        try:
            self._subscribers = self._subscribers + [id]
            if self._recording & (self._stream <> None):
                return self._stream
            else:
                self._start()
                return self._stream
        except Exception as e:
            raise

    def release(self, id):
        if id in self._subscribers:
            self._subscribers.remove(id)
        else:
            print_warning("ID not found in list of subscribers")

        if len(self._subscribers) == 0:
            self.stop()

    def stop(self):
        self._recording = False

    def _start(self):
        self.thread = StoppableThread(target=_record())
        self._recording = True
        self.thread.start()

    def _record(self):
        with picamera.PiCamera() as camera:
            camera.resolution = self.resolution
            camera.start_recording(self.stream, format='h264', quality=23)
            while self._recording:
                camera.wait_recording(15)
                pass
            camera.stop_recording()



Camera = _Camera()
