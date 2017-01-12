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

    def has_tags(self,tags):
        group_tag_match = super(Group,self).has_tags(tags)
        module_tag_match = any(m.has_tags(tags) for m in self.modules)
        return (group_tag_match or module_tag_match)

    def has_action(self,action):
        print_todo("tag argument toevoegen")
        group_has_action = super(Group,self).has_action(action)
        module_has_action = any([m.has_action(action) for m in self.modules])

    def get_actions(self, tags=[]):
        """
            returns a list af all actions posible in this entity and in the modules
            of the group (after a tag-check). Can be used for function suggestion.

            :param list(string) tags:       (optional) list of tags
            :return:                        List of actions
            :rtype:                         list(string)
        """
        actions = []
        if super(Group,self).has_action(action):
            actions = actions + [inspect.getmembers(self, inspect.isfunction)]
            #count the common actions of al modules
            module_actions = {}
            for m in self.modules:
                for a in m.get_actions(tags):
                    if a in module_actions:
                        module_actions[a] = module_actions[a] + 1
                    else:
                        module_actions[a] = 1
            for key,value in module_actions.iteritems():
                if value == len(self.modules):
                    action = action + [key]
        else:
            for m in self.modules:
                actions = actions + m.get_actions(tags)

        actions = list(set(actions))

    def set_mod_dof_value(self,module_name, dof_name, dof_value, anim_time=-1):
        for m in self.modules:
            m.set_mod_dof_value(module_name, dof_name,dof_value,anim_time)

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        for m in self.modules:
            m.set_dof_value(dof_name,dof_value,anim_time)

    def reset_dofs(self):
        for m in self.modules:
            m.reset_dofs()

    def add_module(self, module):
        self.modules = self.modules + [module]

    def get_modules(self,tags=[]):
        result = []
        for m in self.modules:
            if m.has_tags(tags):
                result = result + [m]
        return result
