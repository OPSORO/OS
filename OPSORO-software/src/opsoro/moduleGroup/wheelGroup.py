from opsoro.moduleGroup import moduleGroup
from opsoro.robot import Robot

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

class wheelGroup(moduleGroup):
    """
        helper to control the vehicle. Combines the 4 (or more) wheel modules

        list of function:
            - stop
            - forward
            - backward
            - shortLeft
            - shortRight
            - longLeft
            - longRight
    """

    def __init__(self, name):
        super(self.__class__, self).__init__(name)

    def stop (self, anim_time=-1):
        for w in self.getModules(['all']):
            w.set_dof_value("wheel",0, anim_time)

    def forward(self,speed, anim_time=-1):
        """
            speed = [-1,1]      (-1 means backward)
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)

        for w in self.getModules(['all']):
            print "forward" + str(speed)
            w.set_dof_value("wheel",speed, anim_time)


    def backward(self, speed, anim_time=-1):
        """
            speed = [-1,1]      (-1 means forward)
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.getModules(['all']):
            w.set_dof_value("wheel", -speed, anim_time)

    def shortLeft(self,speed, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.getModules(['left']):
            w.set_dof_value("wheel", -speed, anim_time)
        for w in self.getModules(['right']):
            w.set_dof_value("wheel", speed, anim_time)

    def shortRight(self, speed, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.getModules(['left']):
            w.set_dof_value("wheel", speed, anim_time)
        for w in self.getModules(['right']):
            w.set_dof_value("wheel", -speed, anim_time)

    def longLeft(self,speed, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.getModules(['right']):
            w.set_dof_value("wheel", speed, anim_time)

    def longRight(self, speed, anim_time=-1):
        """
            speed = [-1,1]
            anim_time = time to reach the speed
        """
        speed = constrain(speed,-1,1)
        for w in self.getModules(['left']):
            w.set_dof_value("wheel", speed, anim_time)
