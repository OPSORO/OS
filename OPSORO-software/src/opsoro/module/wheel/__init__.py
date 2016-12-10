from opsoro.module import Module


class Wheel(Module):
    def apply_poly(self, r, phi, anim_time=-1):
        print "apply_poly is not supported for engines"

    def stop(self,anim_time = -1):
        self.set_dof_value("wheel",0,anim_time)

    def forward(self,speed=1,anim_time=-1):
        self.set_dof_value("wheel",speed,anim_time)

    def backward(self,speed=1,anim_time=-1):
        self.set_dof_value("wheel",(-speed),anim_time)
