from opsoro.console_msg import *
from opsoro.dof import DOF
from opsoro.hardware import Hardware


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


class Servo(DOF):
    def config(self, pin=None, min_range=0, mid_pos=1500, max_range=0):
        #, dofname=None):
        """
        Helper class to turn DOF positions into pulse widths for the servo controller.

        :param int pin:         Servo pin number
        :param int min_range:   Minimum range of the servo, can be positive or negative. When dof_pos < 0, pulse width = mid_pos + dof_pos*min_range
        :param int mid_pos:     Pulse width when neutral (DOF position = 0).
        :param int max_range:   Maximum range of the servo, can be positive or negative. When dof_pos > 0, pulse width = mid_pos + dof_pos*max_range
        """
        # dofname:   Name of the DOF that controls the position of this servo
        min_value = 500
        max_value = 2500
        self.pin = int(pin)
        # self.dofname = dofname
        self.mid_pos = int(constrain(int(mid_pos), min_value, max_value))
        self.min_range = int(constrain(int(min_range), min_value - self.mid_pos, max_value - self.mid_pos))
        self.max_range = int(constrain(int(max_range), min_value - self.mid_pos, max_value - self.mid_pos))
        self.position = int(self.mid_pos)

        # print_info(self.__repr__())

    def __repr__(self):
        return "Servo(pin=%d, min_range=%d, mid_pos=%d, max_range=%d)" % (self.pin, self.min_range, self.mid_pos, self.max_range)

    def to_us(self, dof_value=None):
        """
        Converts DOF pos to microseconds.

        :param float dof_value:   value to convert to us. If None; dof value of servo object is used

        :return:         servo value (us)
        :rtype:          int
        """
        own_dof = False
        # Use objects's dof value if provided is None
        if dof_value is None:
            dof_value = self.value
            own_dof = True

        us = int(self.mid_pos)
        dof_value = float(dof_value)

        if dof_value >= 0:
            us += int(dof_value * float(self.max_range))
        else:
            us += int(-dof_value * float(self.min_range))

        if own_dof:
            self.position = us

        return us

    def update(self):
        """
        Updates the servo with the setted dof value.

        :return:         True if dof value is updated, False if dof value did not change
        :rtype:          bool
        """
        dof_animation_changed = super(Servo, self).update()

        # Only update if position is changed
        if self.position == self.to_us():
            return False

        # print_info('Servo: pin: %i, pos: %f' % (self.pin, self.position))

        if self.pin is not None and self.pin >= 0:
            with Hardware.lock:
                Hardware.Servo.set(self.pin, self.position)
                # return True
        return dof_animation_changed
