from opsoro.module import Module


class WheelBase(Module):



    wheelsL = []
    wheelsR = []

    def __init__(self):
        self.name = ""

    def __str__(self):
        return str(self.name)

    def left(self,params):
        pass

    def right(self, parmas):
        pass

    def do(self,params):
        pass

A_TURN_LEFT = left
