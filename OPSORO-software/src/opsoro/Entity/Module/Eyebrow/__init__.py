from opsoro.Entity.Module import Module


class Eyebrow(Module):
    def __init__(self):
        super(Eyebrow,self).__init__(self)
        a = {"set": self.set}
        self.actions.update(a)

    def set(self,value,anim_time=-1):
        value = float(value)
        self.set_dof_value("single",value,anim_time)
