# from opsoro.hardware import Hardware
# from opsoro.dof.servo import Servo
from opsoro.dof import DOF
from opsoro.dof.servo import Servo
from opsoro.dof.engine import Engine
from opsoro.dof.continu_servo import ContinuServo
from opsoro.console_msg import *


from inspect import getargspec
import numpy as np
from scipy import interpolate

import math
import cmath

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class Module(object):
    def __init__(self, data=None):
        self.name = ""
        self.tags = []
        self.position = {}
        self.size = {}
        self.dofs = {}



    def apply_poly(self, r, phi, anim_time=-1):
        for name, dof in self.dofs.iteritems():
            dof.calc(r, phi, anim_time)

    def update(self):
        # index = 0
        updated = False
        for name, dof in self.dofs.iteritems():
            # dof.update(self.dofs[index].value)
            if dof.update():
                updated = True
        return updated

    #not in use
    def execute(self, function, tags=None, *args):
        f = getattr(self, function, None)
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
                    argsValues = []
                    for a in argsList:
                        if a in params:
                            argsValues += [params[str(a)]]
                        else:
                            break
                    f(*[argsValues])
                    return True
                except Exception as e:
                    print_error("Can't find/parse arguments in params")
                    raise
            else:
                print_warning(str(type(self)) + "has no funtion '{}'".format(params["action"]))
        return False

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        if dof_name is None:
            for name, dof in self.dofs.iteritems():
                dof.set_value(dof_value, anim_time)
        elif dof_name in self.dofs:
            self.dofs[dof_name].set_value(dof_value, anim_time)
        else:
            print self.name + " has no dof: " + dof_name


    def set_dof_values(self, dof_values, anim_time=-1):
        """
            set all dofs with same value
            **Sander: ik ben geen fan van deze methode. In de oude versie zat dit volledig in de Robot classe maar door de wijzigingen lukt dit niet.
                      ik zou deze methode liever ombouwen tot een methode 'set_dof_med()' omdat de methode hoofdzakelijk bedoeld is om alle dof's op 0 te plaatsen

        """
        for name, dof in self.dofs.iteritems():
            dof.set_value(name, dof_value, anim_time)


    def has_tags(self,tags):
        if (tags is None) or (tags == []):
            return True
        else:
            return all(x in self.tags for x in tags)



    def __str__(self):
        return str(self.name)
