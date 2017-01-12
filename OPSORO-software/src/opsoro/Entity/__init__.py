import inspect
from inspect import getargspec
from opsoro.console_msg import *

class Entity(object):
    def __init__(self):
        self.name = ""
        self.tags = []

    def update(self):
        pass

    def execute(self, action, tags, **kargs):
        """
            execute function for executing actions on the entity. Checks the
            tags and searches the right methode to call

            :param string action:       name of the function in the Entity
            :param list(string) tags:   tags for selecting the modules
            :param **kargs      extra argumens for function in Entity
        """
        f = getattr(self, action, None)
        if (f is not None) and callable(f):
            f(kargs)
        else:
            print_warning(str(type(self)) + "has no funtion '{}'".format(function))

    def execute(self, params):
        """
            execute function for executing actions on the entity. Checks the
            tags and searches the right methode to call

            :param dict params:     dictionary with the functionname, tags and the arguments
                dict= {
                    "action": "name_of_function_to_execute",
                    "tags": ["tag1","tag2","tag13"],
                    "extra_arg": "value_of_arg",
                    ...
                }
        """
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
        """
            checks if entity has the tags or not

            :param list(string) tags:       list of tags
            :return:                        True if entity contains tags
            :rtype:                         boolean
        """
        if (tags is None) or (tags == []):
            return True
        else:
            return all(x in self.tags for x in tags)

    def has_action(self,action):
        """
            checks if entity has the action or not

            :param string action:           name of function
            :return:                        True if entity contains action
            :rtype:                         boolean
        """
        f = getattr(self, action, None)
        return ( (f is not None) and callable(f))

    def get_actions(self,tags=[]):
        """
            returns a list af all actions posible in this entity. Can be used
            for function suggestion

            :param list(string) tags:       (optional) list of tags
            :return:                        List of actions
            :rtype:                         list(string)
        """
        if self.has_tags(tags):
            return inspect.getmembers(self, inspect.isfunction)

    def set_mod_dof_value(self,module_name, dof_name, dof_value, anim_time=-1):
        """
            Set dof with name 'dof_name' to specific value

            :param string module_name:      Name of the module
            :param string dof_name:         Name of the dof
            :param float dof_value:         Value to set the dof
            :param int anim_time            Duration time of action, negative values means max speed (Default: -1)

        """
        pass

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        """
            Set dof with name 'dof_name' to specific value

            :param string dof_name:         Name of the dof
            :param float dof_value:         Value to set the dof
            :param int anim_time            Duration time of action, negative values means max speed (Default: -1)

        """
        pass

    def reset_dofs(self):
        """
            set all dofs to neutral position
        """
        pass

    def __str__(self):
        result = ""
        result += str(self.name)
        result += "\t"
        result += str(self.tags)
        return result
