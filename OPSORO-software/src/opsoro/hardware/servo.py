from opsoro.hardware import Hardware


import math
import cmath

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class Servo(object):
	def __init__(self, pin=None, min_range=0, mid_pos=1500, max_range=0, dofname=None):
		"""
		Helper class to turn DOF positions into pulse widths for the servo
		controller.

		pin:       Servo pin number
		min_range: Minimum range of the servo, can be positive or negative.
		           When dof_pos = -1.0, pulse width = mid_pos + dof_pos*min_range
		mid_pos:   Pulse width when neutral (DOF position = 0).
		max_range: Maximum range of the servo, can be positive or negative.
		           When dof_pos = 1.0, pulse width = mid_pos + dof_pos*max_range
		dofname:   Name of the DOF that controls the position of this servo
		"""
		min_value = 500
		max_value = 2500
		self.pin = pin
		self.dofname = dofname
		self.mid_pos =  constrain(mid_pos, min_value, max_value)
		self.min_range = constrain(min_range, min_value-self.mid_pos, max_value-self.mid_pos)
		self.max_range = constrain(max_range, min_value-self.mid_pos, max_value-self.mid_pos)
		self.value = self.mid_pos

	def __repr__(self):
		return "Servo(pin=%d, min_range=%d, mid_pos=%d, max_range=%d, dofname=%s)" % (self.pin, self.min_range, self.mid_pos, self.max_range, self.dofname)

	def dof_to_us(self, dof_pos):
		"""Converts DOF pos to microseconds. DOF pos from -1.0 to 1.0."""
		# TODO: is int() necessary? Check later if return value can be float
		if dof_pos >= 0:
			self.value = int(self.mid_pos + dof_pos * self.max_range)
		else:
			self.value = int(self.mid_pos + -dof_pos * self.min_range)

		return self.value

	def update(self):
		with Hardware.lock:
			Hardware.servo_set(self.pin, self.value)
