
class Camera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.csystems = []
