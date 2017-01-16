from opsoro.Entity.Module import Module


class Wheel(Module):
    def __init__(self):
        super(Wheel,self).__init__()
        self.actions.update({"stop":self.stop,
                              "forward":self.forward,
                              "backward":self.backward})

    def apply_poly(self, r, phi, anim_time=-1):
        print "apply_poly is not supported for engines"

    def stop(self,anim_time = -1):
        self.set_dof_value("single",0,anim_time)

    def forward(self,speed=1,anim_time=-1):
        self.set_dof_value("single",speed,anim_time)

    def backward(self,speed=1,anim_time=-1):
        self.set_dof_value("single",(-speed),anim_time)
