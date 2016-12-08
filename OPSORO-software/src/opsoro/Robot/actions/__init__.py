
import drive


class _Actions(object):

    class _drive:

        def stop(self, anim_time=-1):
            for w in self.getModules(['all']):
                w.set_dof_value("wheel", 0, anim_time)

        def forward(self, speed, anim_time=-1, tags=['all']):
            """
                speed = [-1,1]      (-1 means backward)
                anim_time = time to reach the speed
            """
            speed = constrain(speed, -1, 1)

            for w in self.getModules(tags):
                print "forward" + str(speed)
                w.set_dof_value("wheel", speed, anim_time)

        def backward(self, speed, anim_time=-1, tags=['all']):
            """
                speed = [-1,1]      (-1 means forward)
                anim_time = time to reach the speed
            """
            speed = constrain(speed, -1, 1)
            for w in self.getModules(tags):
                w.set_dof_value("wheel", -speed, anim_time)

        def shortLeft(self, speed, anim_time=-1):
            """
                speed = [-1,1]
                anim_time = time to reach the speed
            """
            speed = constrain(speed, -1, 1)
            for w in self.getModules(['left']):
                w.set_dof_value("wheel", -speed, anim_time)
            for w in self.getModules(['right']):
                w.set_dof_value("wheel", speed, anim_time)

        def shortRight(self, speed, anim_time=-1):
            """
                speed = [-1,1]
                anim_time = time to reach the speed
            """
            speed = constrain(speed, -1, 1)
            for w in self.getModules(['left']):
                w.set_dof_value("wheel", speed, anim_time)
            for w in self.getModules(['right']):
                w.set_dof_value("wheel", -speed, anim_time)

        def longLeft(self, speed, anim_time=-1):
            """
                speed = [-1,1]
                anim_time = time to reach the speed
            """
            speed = constrain(speed, -1, 1)
            for w in self.getModules(['right']):
                w.set_dof_value("wheel", speed, anim_time)

        def longRight(self, speed, anim_time=-1):
            """
                speed = [-1,1]
                anim_time = time to reach the speed
            """
            speed = constrain(speed, -1, 1)
            for w in self.getModules(['left']):
                w.set_dof_value("wheel", speed, anim_time)
    drive = _drive()


actions = _Actions()