from __future__ import division

from bisect import bisect_right
import math

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

def interpolate(xa, xb, ya, yb, x):
		return ya + (yb - ya)*(x-xa)/(xb-xa)

def normalizeAngle(angle):
		angle = angle % 360
		angle = (angle + 360) % 360
		return angle

class DOF(object):
	def __init__(self, em, mid_pos=1500, min_range=-1000, max_range=1000):
		self.em = em # Reference to the Expression Manager

		self.min_range = min_range
		self.mid_pos = mid_pos
		self.max_range = max_range

		# Variables for tweening
		self.pos_start = 0
		self.pos_target = 0
		self.pos_current = 0

		self.tween_currrent = 0
		self.tween_target = 0

	def min(self):
		return self.mid_pos + self.min_range

	def mid(self):
		return self.mid_pos

	def max(self):
		return self.mid_pos + self.max_range

	def __int__(self):
		if self.pos_current >= 0:
			#return int(interpolate(0, 100, self.midpwm, self.maxpwm, pos))
			return int(self.mid_pos + (self.max_range * (self.pos_current/100)))
		else:
			#return int(interpolate(-100, 0, self.minpwm, self.midpwm, pos))
			return int(self.mid_pos + (self.min_range * (self.pos_current/-100)))

	def set_target_pos(self, pos, steps=0):
		pos = constrain(pos, -100, 100)
		if steps == 0:
			# No tweening necessary, no steps
			self.pos_start = pos
			self.pos_current = pos
			self.pos_target = pos
			self.tween_currrent = 0
			self.tween_target = 0
			return
		elif self.tween_target == 0 and self.pos_current == pos:
			# No tween necessary, already at pos
			return
		else:
			self.pos_start = self.pos_current
			self.pos_target = pos
			self.tween_currrent = 0
			self.tween_target = steps

	def step(self):
		if self.tween_target == 0:
			# Not tweening
			return

		self.tween_currrent += 1

		if self.tween_currrent >= self.tween_target:
			# End of tween reached
			self.pos_current = self.pos_target
			self.pos_start = self.pos_target
			self.tween_currrent = 0
			self.tween_target = 0
			return
		else:
			self.pos_current = interpolate(0, self.tween_target, self.pos_start, self.pos_target, self.tween_currrent)
			return

class EyeHorDOF(DOF):
	def __int__(self):
		return super(EyeHorDOF, self).__int__()

	def set_target_eye(self, steps=0):
		self.set_target_pos(self.em.eye_hor, steps)

class EyeVerDOF(DOF):
	def __int__(self):
		self.pos = self.em.eye_ver
		return super(EyeVerDOF, self).__int__()

	def set_target_eye(self, steps=0):
		self.set_target_pos(self.em.eye_ver, steps)

class MapDOF(DOF):
	def __init__(self, em, neutral, poly, mid_pos=1500, min_range=-1000, max_range=1000):
		self.neutral = neutral
		self.poly = poly
		self.sortedkeys = sorted(poly.keys())

		self.alpha = 0
		self.length = 0

		super(MapDOF, self).__init__(em, mid_pos, min_range, max_range)

	def alpha_to_pos(self, alpha):
		alpha = normalizeAngle(alpha)

		if len(self.poly) == 0:
			# Empty list, return neutral position
			return self.neutral
		if len(self.poly) == 1:
			# Only one item, return that item
			return self.poly.values()[0]

		idxHigher = bisect_right(self.sortedkeys, alpha)

		if idxHigher == 0 or idxHigher == len(self.sortedkeys):
			lower = self.sortedkeys[-1]
			higher = self.sortedkeys[0]
			return interpolate(lower, higher + 360, self.poly[lower], self.poly[higher], alpha)
		else:
			lower = self.sortedkeys[idxHigher - 1]
			higher = self.sortedkeys[idxHigher]
			return interpolate(lower, higher, self.poly[lower], self.poly[higher], alpha)

	def alpha_length_to_pos(self, alpha, length):
		pos = self.alpha_to_pos(alpha)
		pos = interpolate(0.0, 1.0, self.neutral, pos, length)
		return pos

	def set_target_alpha_length(self, alpha, length, steps=0):
		pos = self.alpha_length_to_pos(alpha, length)
		self.set_target_pos(pos, steps)

	def set_target_valence_arousal(self, valence, arousal, steps=0):
		length = math.sqrt(valence*valence + arousal*arousal)

		alpha = math.atan2(arousal, valence)
		if alpha < 0:
			alpha += 2*math.pi;
		alpha = math.degrees(alpha)

		length = constrain(length, 0.0, 1.0)
		alpha = normalizeAngle(alpha)

		self.set_target_alpha_length(alpha, length, steps)
