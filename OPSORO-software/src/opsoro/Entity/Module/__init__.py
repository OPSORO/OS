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
        updated = False
        for name, dof in self.dofs.iteritems():
            if dof.update():
                updated = True
        return updated

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        if dof_name in self.dofs:
            self.dofs[dof_name].set_value(dof_value, anim_time)


    def reset_dofs(self):
        for name, dof in self.dofs.iteritems():
            dof.set_value(name, 0, anim_time)
