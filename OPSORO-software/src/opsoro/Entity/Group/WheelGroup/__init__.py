from opsoro.Entity.Group import Group
constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

class WheelGroup(Group):

    def __init__(self):
        super(WheelGroup,self).__init__()
        a = {               "stop":self.stop,
                              "forward":self.forward,
                              "backward":self.backward,
                              "shortLeft":self.shortLeft,
                              "shortRight":self.shortRight,
                              "longLeft":self.longLeft,
                              "longRight":self.longRight}
        self.actions.update(a)


    def stop (self, anim_time=-1):
        for w in self.get_modules():
            w.set_dof_value("single",0, anim_time)

    def forward(self,speed=1, anim_time=-1):
        """"
        speed = [-1,1]      (-1 means backward)
        anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)

        for w in self.get_modules():
            w.set_dof_value("single",speed, anim_time)


    def backward(self, speed=1, anim_time=-1):
        """
        speed = [-1,1]      (-1 means forward)
        anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules():
            w.set_dof_value("single", -speed, anim_time)

    def shortLeft(self,speed=1, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules(['left']):
            w.set_dof_value("single", -speed, anim_time)
        for w in self.get_modules(['right']):
            w.set_dof_value("single", speed, anim_time)

    def shortRight(self, speed=1, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules(['left']):
            w.set_dof_value("single", speed, anim_time)
        for w in self.get_modules(['right']):
            w.set_dof_value("single", -speed, anim_time)

    def longLeft(self,speed=1, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules(['right']):
            w.set_dof_value("single", speed, anim_time)

    def longRight(self, speed=1, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules(['left']):
            w.set_dof_value("single", speed, anim_time)
