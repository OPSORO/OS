# from opsoro.hardware import Hardware
from opsoro.console_msg import *

import numpy as np
from scipy import interpolate

from opsoro.animate import Animate

import math
import cmath

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class DOF(object):
    def __init__(self, name, neutral=0.0, poly=None):
        self.name = name
        self.value = neutral

        # Dict to store any extra data from YAML files
        self.data = {}

        # List of overlay functions
        # def my_overlay(dofpos, dof):
        #   new_dof_pos = dofpos
        #   return my_new_pos
        self.overlays = []

        self._neutral = None
        self._interp_poly = None

        self._anim = None

        # Update control polygon
        self.set_control_polygon(neutral, poly)

    def config(self, **args):
        pass

    def __repr__(self):
        return "DOF(name=%s, neutral=%.2f, poly={...})" \
         % (self.name, self._neutral)

    def set_control_polygon(self, neutral=0.0, poly=None):
        self._neutral = constrain(neutral, -1.0, 1.0)

        if poly is None or len(poly) == 0:
            self._interp_poly = lambda x: self._neutral
        else:
            phis = np.linspace(-math.pi, math.pi, 20)[0:20]
            dofs = map(lambda x: float(x), poly)

            # Sort lists
            indexes = range(len(phis))
            indexes.sort(key=phis.__getitem__)
            sorted_phis = map(phis.__getitem__, indexes)
            sorted_dofs = map(dofs.__getitem__, indexes)

            # Create interpolation instance
            self._interp_poly = interpolate.interp1d(
                sorted_phis, sorted_dofs, kind="linear")

    def calc(self, r, phi, anim_time=-1):
        # print_info('Calc; r: %d, phi: %d, time: %i' % (r, phi, anim_time))
        # Calculate DOF position at max intensity

        if phi > 0:
            phi -= math.pi
        elif phi <= 0:
            phi += math.pi

        dof_at_max_r = float(self._interp_poly(phi))

        # Interpolate between neutral DOF pos and max intensity DOF pos
        self.set_value(
            float(self._neutral) + (r * (dof_at_max_r - float(self._neutral))),
            anim_time)

        # Execute overlays
        for overlay_fn in self.overlays:
            try:
                self.set_value(overlay_fn(self.value, self), anim_time)
            except TypeError:
                # Not a callable object, or function does not take 2 args
                pass

        return self.value

    def set_value(self, dof_value=0, anim_time=-1):
        # print_info('Set value: %d, time: %i' % (dof_value, anim_time))

        dof_value = float(constrain(float(dof_value), -1.0, 1.0))
        # Apply transition animation
        if anim_time < 0:
            anim_time = float(abs(dof_value - float(self.value))) / 3.0

        self._anim = Animate([0, anim_time], [self.value, dof_value])

    def update(self):
        """
        Updates the dof value according to the animation

        returns:    boolean
                    True if dof value is updated
                    False if dof value did not change
        """
        if self._anim is not None:
            self.value = float(self._anim())
            if self._anim is None or self._anim.has_ended():
                self._anim = None
            return True
        return False

    # def add_overlay(self, fn):
    #     self.overlays.append(fn)
    #
    # def remove_overlay(self, fn):
    #     self.overlays.remove(fn)
    #
    # def clear_overlays(self):
    #     self.overlays = []
