from opsoro.Entity.Module import Module


class Eye(Module):
    def __init__(self):
        super(Eye,self).__init__(self)
        a = {"close": self.close,"open":self.open, "look_at":self.look_at, "set":self.set_closure}
        self.actions.update(a)


    def close(self,anim_time=-1):
        self.set_dof_value("eyelid_closure",-1,anim_time)

    def open(self,anim_time=-1):
        self.set_dof_value("eyelid_closure",0,anim_time)

    def look_at(self,hor,vert,anim_time=-1):
        self.set_dof_value("pupil_horizontal",hor,anim_time)
        self.set_dof_value("pupil_vertical",vert,anim_time)
        pass

    def set_closure(self,value,anim_time=-1):
        value = float(value)
        self.set_dof_value("eyelid_closure",value,anim_time)
