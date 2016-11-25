from opsoro.hardware import Hardware
from opsoro.console_msg import *
from opsoro.dof import DOF

import math
import cmath

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class Engine(DOF):

    def config(self, pin_a,pin_b, min_speed = 500, max_speed = 2500, reverse = False):
        """
        pin_a: a pin of the engine
        pin_b: b pin of the engine
        min_speed: the minimum speed to the engine depending on the load
        max_speed: the maximum speed of the engine
        reverse: turning clockwise = False;
		"""

        self.pin_a = int(pin_a)
        self.pin_b = int(pin_b)
        self.min_speed = int(min_speed)
        self.max_speed = int(max_speed)
        self.reverse = boolean(reverse)
        self.speed = 0


    def __repr__(self):
        return "Engine(pin_a=%d, pin_b=%d, min_speed=%d, max_speed=%d, reverse=%d)" % (
            self.pin_a,self.pin_b, self.min_speed, self.max_speed, self.reverse)

    def dof_to_us(self, dof_value):
        if dof_value == 0:
            return 0
        elif dof_value > 0:
            return ((self.max_speed-self.min_speed)*dof_value)-self.min_speed
        else:
            return ((self.max_speed-self.min_speed)*dof_value)+self.min_speed


    def update(self):
        """
        update self.value to engine
        returns:    boolean
                    True if dof value is updated
                    False if dof value did not change
        """
        dof_animation_changed = super(Engine, self).update()

        if (dof_animation_changed == False) & (self.speed == dof_to_us(self.value)):
            return False
        else:
            self.speed = dof_to_us(self.value)
            if(self.speed == 0):
                with Hardware.lock:
                    Hardware.servo_set(self.pin_a, 0)
                    Hardware.servo_set(self.pin_b, 0)
            elif (reverse == False) ^ (self.speed > 0 ):
                with Hardware.lock:
                    Hardware.servo_set(self.pin_a, 0)
                    Hardware.servo_set(self.pin_b,self.speed)
            else:
                with Hardware.lock:
                    Hardware.servo_set(self.pin_a, self.speed)
                    Hardware.servo_set(self.pin_b,0)
            return True
