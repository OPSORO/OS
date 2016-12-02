from opsoro.stoppable_thread import StoppableThread
from opsoro.console_msg import *
import datatime
import picamera

class _Camera(object):

    def __init__(self):
        self.camera = picamera.PiCamera()

    def takePicture(self, path = _fileName()):
        self.cap.capture(path,format='jpeg')
        print_info "image saved: {}".format(path)

    
    def _fileName():
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        path = "data/images/" + filenam

    def _del_(self):
        self.camera.

Camera = _Camera()
