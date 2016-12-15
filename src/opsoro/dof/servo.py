from opsoro.hardware import Hardware
from opsoro.console_msg import *
from opsoro.dof import DOF

import math
import cmath

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class Servo(DOF):
    def config(self, pin=None, min_range=0, mid_pos=1500, max_range=0):
        #, dofname=None):
        """
		Helper class to turn DOF positions into pulse widths for the servo
		controller.

		pin:       Servo pin number
		min_range: Minimum range of the servo, can be positive or negative.
		           When dof_pos < 0, pulse width = mid_pos + dof_pos*min_range
		mid_pos:   Pulse width when neutral (DOF position = 0).
		max_range: Maximum range of the servo, can be positive or negative.
		           When dof_pos > 0, pulse width = mid_pos + dof_pos*max_range
		"""
        # dofname:   Name of the DOF that controls the position of this servo
        min_value = 500
        max_value = 2500
        self.pin = int(pin)
        # self.dofname = dofname
        self.mid_pos = int(constrain(int(mid_pos), min_value, max_value))
        self.min_range = int(
            constrain(
                int(min_range), min_value - self.mid_pos, max_value -
                self.mid_pos))
        self.max_range = int(
            constrain(
                int(max_range), min_value - self.mid_pos, max_value -
                self.mid_pos))
        self.position = int(self.mid_pos)

        # print_info(self.__repr__())

    def __repr__(self):
        return "Servo(pin=%d, min_range=%d, mid_pos=%d, max_range=%d)" % (
            self.pin, self.min_range, self.mid_pos, self.max_range)

    def to_us(self):
        """
        Converts DOF pos to microseconds.

        returns:
            servo value (us)
        """
        self.position = self.dof_to_us(self.value)

        return self.position

    def dof_to_us(self, dof_value):
        """
        Converts DOF pos to microseconds.

        returns:
            servo value (us)
        """
        us = int(self.mid_pos)
        dof_value = float(dof_value)

        if dof_value >= 0:
            us += int(dof_value * float(self.max_range))
        else:
            us += int(-dof_value * float(self.min_range))

        return us

    def update(self):
        """
        Updates the servo with the dof value.

        returns:    boolean
                    True if dof value is updated
                    False if dof value did not change
        """
        dof_animation_changed = super(Servo, self).update()

        # Only update if position is changed
        if self.position == self.to_us():
            return False

        # print_info('Servo: pin: %i, pos: %f' % (self.pin, self.position))

        if self.pin is not None:
            with Hardware.lock:
                Hardware.servo_set(self.pin, self.position)
                # return True
        return dof_animation_changed
