import inspect
from inspect import getargspec
from opsoro.console_msg import *

class Entity(object):
    def __init__(self):
        self.name = ""
        self.tags = []

    def update(self):
        pass

    def execute(self, action, tags, **args):
        f = getattr(self, action, None)
        if (f is not None) and callable(f):
            f(args)
        else:
            print_warning(str(type(self)) + "has no funtion '{}'".format(function))

    def execute(self, params):
        action = (params["action"] if "action" in params else None)
        if action:
            f = getattr(self, params["action"], None)
            if (f is not None) and callable(f):
                try:
                    argsList = getargspec(f)[0][1:]
                    argsValues = {}
                    for a in argsList:
                        if a in params:
                            argsValues[str(a)] = params[str(a)]

                    if len(argsValues) >0:
                        f(**argsValues)
                    else:
                        f()
                    return True
                except Exception as e:
                    print_error("Can't find/parse arguments in params")
                    raise
            else:
                print_warning(str(type(self)) + "has no funtion '{}'".format(params["action"]))
        return False


    def has_tags(self,tags):
        if (tags is None) or (tags == []):
            return True
        else:
            return all(x in self.tags for x in tags)

    def has_action(self,action):
        f = getattr(self, action, None)
        return ( (f is not None) and callable(f))

    def get_actions(self,tags=[]):
        if self.has_tags(tags):
            return inspect.getmembers(self, inspect.isfunction)


    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        pass

    def reset_dofs(self):
        pass

    def __str__(self):
        result = ""
        result += str(self.name)
        result += "\t"
        result += str(self.tags)
        return result
