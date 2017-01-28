from opsoro.Entity import Entity
from opsoro.console_msg import *
from inspect import getargspec

class Group(Entity):
    """
        definition of functions SEE ENTITY.__init__
    """
    def __init__(self):
        super(Group,self).__init__()
        self.modules = []


    def update(self):
        return any([m.update() for m in self.modules])

    def execute(self, params):
        executed = False
        action = (params["action"] if "action" in params else None)
        tags = (params["tags"] if "tags" in params else None)
        if action and tags:
            if self.has_tags(tags) == 1:
                 executed = super(Group,self).execute(params)
            if self.has_tags(tags) >= 1:
                modules = self.get_modules(tags)
                e = []
                for m in modules:
                    r = m.execute(params)
                    e += [r]
                executed = all(e)
        else:
            print_warning("can't find parameters: " + str(params))

        return executed

    def has_tags(self,tags):
        if super(Group,self).has_tags(tags) == 1:
            return 1
        elif any(m.has_tags(tags) for m in self.modules):
            return 2
        else:
            return 0


    def has_action(self,action):
        return (action in self.get_actions())

    def get_actions(self, tags=[]):
        """
            returns a list af all actions posible in this entity and in the modules
            of the group (after a tag-check). Can be used for function suggestion.

            :param list(string) tags:       (optional) list of tags
            :return:                        List of actions
            :rtype:                         list(string)
        """
        result = []

        modules = self.get_modules(tags)
        result += [m.get_actions() for m in modules]
        if self.has_tags(tags) == 1:
            tmp = super(Group,self).get_actions(tags)
            result += tmp

        #TO DO: remove duplicates
        return result


    def set_mod_dof_value(self,module_name, dof_name, dof_value, anim_time=-1):
        for m in self.modules:
            m.set_mod_dof_value(module_name, dof_name,dof_value,anim_time)

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        for m in self.modules:
            m.set_dof_value(dof_name,dof_value,anim_time)

    def set_all_dofs(self,dof_value, anim_time=-1):
        for m in self.modules:
            m.set_all_dofs(dof_value, anim_time)

    def reset_dofs(self):
        for m in self.modules:
            m.reset_dofs()

    def apply_poly(self, r, phi, anim_time=-1):
        for m in self.modules:
            m.apply_poly(r,phi,anim_time)

    def add_module(self, module):
        self.modules = self.modules + [module]

    def get_modules(self,tags=[]):
        result = []
        for m in self.modules:
            if m.has_tags(tags) > 0:
                result = result + [m]
        return result
