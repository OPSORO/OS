from opsoro.hardware import Hardware
from opsoro.console_msg import *
from opsoro.dof import DOF

import math
import cmath

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


#wordt niet meer gebruikt
class ContinuServo(DOF):
    def config(self, pin=None, forward_pers=0, mid_pos=1500, backward_pers=0, reverse=False):
        """
		Helper class to turn DOF positions into pulse widths for the servo
		controller.

		pin:                Servo pin number
		forward_pers:       percentage forward (fulspeed = 100)
		mid_pos:            Pulse width when neutral (DOF position = 0).
		backward_pers:      percentage backward (fulspeed = 100)

        in range from max_range => car drives forward
        in range from min_range => car drives backward

        |500|-------------------------------------|mid_pos|--------------------------------|2500|
                    [mid_pos - min_range]                        [mid_pos + max_range]
                    => backward                                  => forward
		"""
        min_value = 500
        max_value = 2500
        forward_pers = int(forward_pers)
        backward_pers = int(backward_pers)
        mid_pos = int(mid_pos)

        self.pin = int(pin)
        self.mid_pos = int(constrain(int(mid_pos), min_value, max_value))
        self.min_range = int((mid_pos - min_value) * (constrain(backward_pers, 0.0, 100.0)/100.0))
        self.max_range = int((max_value - mid_pos) * (constrain(forward_pers, 0.0, 100.0)/100.0))
        self.position = int(self.mid_pos)
        self.reverse = bool(reverse)

    def __repr__(self):
        return "ContinuServo(pin={}, min_range={}, mid_pos={}, max_range={}, reverse={})".format(
            self.pin, self.min_range, self.mid_pos, self.max_range, self.reverse)

    def dof_to_us(self, dof_value):
        """
        Converts DOF pos to microseconds.
        reverse==True will reverse the direction of rotation, so [min_range,mid_pos] is always backward

        returns:
            servo value (us)
        """
        us = int(self.mid_pos)
        dof_value = float(dof_value)
        if dof_value == 0:
            pass
        elif (self.reverse == False) ^ (dof_value > 0 ):
            us += int(abs(dof_value) * float(self.max_range))
        else:
            us -= int(abs(dof_value) * float(self.min_range))
        return us

    def update(self):
        """
        Updates the servo with the dof value.

        returns:    boolean
                    True if dof value is updated
                    False if dof value did not change
        """
        dof_animation_changed = super(ContinuServo, self).update() #change self.value

        # Only update if position is changed
        if self.position == self.dof_to_us(self.value):
            return False
        else:
            self.position = self.dof_to_us(self.value)



        if self.pin is not None:
            with Hardware.lock:
                Hardware.servo_set(self.pin, self.position)
                # return True
        return dof_animation_changed
