# from opsoro.hardware import Hardware
import math
import time

from scipy import interpolate

from opsoro.animate import Animate
from opsoro.console_msg import *


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


class DOF(object):
    def __init__(self, name, neutral=0.0, poly=None):
        """
        DOF class.

        :param string name:     name of the DOF.
        :param float neutral:   neutral dof position.
        :param list poly:       20 dof values linked to emotions.
        """

        self.name = name
        self.tags = []
        self.value = neutral
        self.to_value = neutral

        # Dict to store any extra data from YAML files
        self.data = {}

        # # List of overlay functions
        # # def my_overlay(dofpos, dof):
        # #   new_dof_pos = dofpos
        # #   return my_new_pos
        # self.overlays = []

        self._neutral = None
        self._interp_poly = None

        self._anim = None

        # Update control polygon
        self.set_control_polygon(neutral, poly)

        self.last_set_time = int(round(time.time() * 1000))
        self.last_set_value = neutral

    def config(self, **args):
        pass

    def __repr__(self):
        return "DOF(name=%s, neutral=%.2f, poly={...})" \
            % (self.name, self._neutral)

    def set_control_polygon(self, neutral=0.0, poly=None):
        """
        Sets the control polygon, 20 dof values are linked to certain emotions.

        :param float neutral:   neutral dof position.
        :param list poly:       20 dof values linked to emotions.
        """

        self._neutral = constrain(neutral, -1.0, 1.0)

        if poly is None or len(poly) == 0:
            self._interp_poly = lambda x: self._neutral
        else:
            dofs = map(lambda x: float(x), poly)

            # Fixed phis, this is currently always the same
            phis = [
                -3.1415926535897931, -2.8108986900540254, -2.4802047265182576,
                -2.1495107629824899, -1.8188167994467224, -1.4881228359109546,
                -1.1574288723751871, -0.82673490883941936,
                -0.49604094530365161, -0.16534698176788387,
                0.16534698176788387, 0.49604094530365161, 0.82673490883941891,
                1.1574288723751867, 1.4881228359109544, 1.8188167994467221,
                2.1495107629824899, 2.4802047265182576, 2.8108986900540254,
                3.1415926535897931
            ]
            # Sort lists
            indexes = range(len(phis))
            sorted_dofs = map(dofs.__getitem__, indexes)

            # Create interpolation instance
            self._interp_poly = interpolate.interp1d(phis, sorted_dofs, kind="linear")

    def calc(self, r, phi, anim_time=-1):
        """
        Calculate dof value with the polygon, according to the given r and phi.

        :param float r:         radius r, intensity of the emotion.
        :param float phi:       (radians) angle of the emotion in the circumplex.
        :param float anim_time: time for the servo to move from previous dof to the new dof (-1: animation will be based on dof differences).
        """
        # print_info('Calc; r: %d, phi: %d, time: %i' % (r, phi, anim_time))
        # Calculate DOF position at max intensity

        if phi > 0:
            phi -= math.pi
        elif phi <= 0:
            phi += math.pi

        dof_at_max_r = float(self._interp_poly(phi))

        # Interpolate between neutral DOF pos and max intensity DOF pos
        self.set_value(float(self._neutral) + (r * (dof_at_max_r - float(self._neutral))), anim_time)

        # # Execute overlays
        # for overlay_fn in self.overlays:
        #     try:
        #         self.set_value(overlay_fn(self.value, self), anim_time)
        #     except TypeError:
        #         # Not a callable object, or function does not take 2 args
        #         pass

    def set_value(self, dof_value=0, anim_time=-1, is_overlay=False, update_last_set_time=True):
        """
        Sets the dof value.

        :param float dof_value:             new value of the dof.
        :param float anim_time:             time for the servo to move from previous dof to the new dof (-1: animation will be based on dof differences).
        :param bool is_overlay:             used to determine what priority the dof value has (overlay > default).
        :param bool update_last_set_time:   update the last set timer of the dof.
        """
        # print_info('Set value: %d, time: %i' % (dof_value, anim_time))

        dof_value = float(constrain(float(dof_value), -1.0, 1.0))
        self.to_value = dof_value

        # Apply transition animation
        if anim_time < 0:
            anim_time = float(abs(dof_value - float(self.value))) / 1.0

        self._anim = Animate([0, anim_time], [self.value, dof_value])

        if not is_overlay:
            self.last_set_value = dof_value

        if update_last_set_time:
            self.last_set_time = int(round(time.time() * 1000))

    def set_overlay_value(self, dof_value=0, anim_time=-1, update_last_set_time=True):
        """
        Sets the overlay value and overwrites the dof position.

        :param float dof_value:             new overlay value of the dof.
        :param float anim_time:             time for the servo to move from previous dof to the new dof (-1: animation will be based on dof differences).
        :param bool update_last_set_time:   update the last set timer of the dof.
        """
        self.set_value(dof_value, anim_time, True, update_last_set_time)

    def reset_overlay(self, anim_time=-1):
        """
        Clears the overlay value and resets the dof position to the last set value.

        :param float anim_time: time for the servo to move from previous dof to the new dof (-1: animation will be based on dof differences).
        """

        self.set_value(self.last_set_value, anim_time)

    def update(self):
        """
        Updates the dof value according to the animation.

        :return:    True if dof value is updated, False if dof value did not change.
        :rtype:     bool
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
