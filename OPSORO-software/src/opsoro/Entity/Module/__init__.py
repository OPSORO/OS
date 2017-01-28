from opsoro.dof import DOF
from opsoro.dof.servo import Servo
from opsoro.dof.engine import Engine
from opsoro.dof.continu_servo import ContinuServo
from opsoro.console_msg import *

from opsoro.Entity import Entity

from inspect import getargspec
import numpy as np
from scipy import interpolate

import math
import cmath

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class Module(Entity):
    """
        definition of functions SEE ENTITY.__init__
    """
    def __init__(self, data=None):
        super(Module,self).__init__()
        self.name = ""
        self.tags = []
        self.position = {}  #not implemented
        self.size = {}      #not implemented
        self.dofs = {}

    def apply_poly(self, r, phi, anim_time=-1):
        for name, dof in self.dofs.iteritems():
            dof.calc(r, phi, anim_time)

    def update(self):
        updated = False
        for name, dof in self.dofs.iteritems():
            if dof.update():
                updated = True
        return updated

    def set_mod_dof_value(self,module_name, dof_name, dof_value, anim_time=-1):
        if self.name == module_name:
            self.set_dof_value(dof_name, dof_value, anim_time)

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        if dof_name in self.dofs:

            self.dofs[dof_name].set_value(dof_value, anim_time)

    def set_all_dofs(self,dof_value, anim_time=-1):
        for d in self.dofs:
            self.dofs[d].set_value(dof_value, anim_time)


    def reset_dofs(self):
        for name, dof in self.dofs.iteritems():
            dof.set_value(0.20)
            dof.set_value(0)

    def execute(self, params):
        if super(Module,self).execute(params):
            return True
        else:
            print_warning(str(type(self)) + "has no funtion '{}'".format(params["action"]))
            return False
