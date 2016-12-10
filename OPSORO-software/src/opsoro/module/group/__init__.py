from opsoro.module import Module
from opsoro.console_msg import *
from inspect import getargspec

class Group(Module):
    def __init__(self,data=None):
        super(Group,self).__init__(data)
        self.modules = []
        self.module_names = []

    def add(self, name):
        self.modules += name

    def execute(self, params):
        executed = super(Group, self).execute(params)
        action = (params["action"] if "action" in params else None)
        tags = (params["tags"] if "tags" in params else None)
        if action and tags and not executed :
            modules = self.getModules(tags)
            executed = []
            for m in modules:
                r = m.execute(params)
                executed += [r]
            executed = all(executed)
        return executed

    def getModules(self,tags=[]):
        result = []
        for m in self.modules:
            if m.has_tags(tags):
                result = result + [m]

        return result

    def update(self):
        pass

    def apply_poly(self, r, phi, anim_time=-1):
        for m in self.modules:
            m.apply_poly(r,phi,anim_time)

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        for m in self.modules:
            m.set_dof_value(dof_name,dof_value,anim_time)


    def set_dof_values(self, dof_values, anim_time=-1):
        """
            set all dofs with same value
            **Sander: zie opmerking module.__init__
        """
        for m in self.modules:
            m.set_values(dof_value, anim_time)
