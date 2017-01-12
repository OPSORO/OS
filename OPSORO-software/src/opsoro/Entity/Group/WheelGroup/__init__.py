from opsoro.Entity.Group import Group
constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

class WheelGroup(Group):

    def stop (self, anim_time=-1):
        for w in self.get_modules():
            w.set_dof_value("single",0, anim_time)

    def forward(self,speed=0.5, anim_time=-1):
        """
            speed = [-1,1]      (-1 means backward)
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)

        for w in self.get_modules():
            w.set_dof_value("wheel",speed, anim_time)


    def backward(self, speed=1, anim_time=-1):
        """
            speed = [-1,1]      (-1 means forward)
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules():
            w.set_dof_value("wheel", -speed, anim_time)

    def shortLeft(self,speed=1, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules(['left']):
            w.set_dof_value("wheel", -speed, anim_time)
        for w in self.get_modules(['right']):
            w.set_dof_value("wheel", speed, anim_time)

    def shortRight(self, speed=1, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules(['left']):
            w.set_dof_value("wheel", speed, anim_time)
        for w in self.get_modules(['right']):
            w.set_dof_value("wheel", -speed, anim_time)

    def longLeft(self,speed=1, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules(['right']):
            w.set_dof_value("wheel", speed, anim_time)

    def longRight(self, speed=1, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.get_modules(['left']):
            w.set_dof_value("wheel", speed, anim_time)
