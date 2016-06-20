from __future__ import division
from __future__ import with_statement

import math
import cmath
import os
import threading
from functools import partial

import numpy as np
from scipy import interpolate

from animate import Animate
from hardware import Hardware
from console_msg import *

import yaml
try:
	from yaml import CLoader as Loader
	print_info("Using YAML CLoader")
except ImportError:
	print_info("YAML CLoader not available, falling back on python implementation")
	from yaml import Loader

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

# Config file locations
_configs = {
	"pinmap":     get_path("config/pinmap.yaml"),
	"limits":     get_path("config/limits.yaml"),
	"functions":  get_path("config/functions.yaml")
}

class DOF(object):
	def __init__(self, name, neutral=0.0, poly=None):
		self.name = name
		self.cached_pos = neutral

		# Dict to store any extra data from YAML files
		self.data = {}

		# List of overlay functions
		# def my_overlay(dofpos, dof):
		#   new_dof_pos = dofpos
		#   return my_new_pos
		self.overlays = []

		self._phis = None
		self._dofs = None
		self._neutral = None
		self._interp_poly = None

		self.set_control_polygon(neutral, poly)

	def __repr__(self):
		return "DOF(name=%s, neutral=%.2f, poly={...})" \
		 % (self.name, self._neutral)

	def set_control_polygon(self, neutral=0.0, poly=None):
		def deg_to_rad_minpi_pluspi(deg):
			# Convert to [0, 360[
			deg = deg % 360.0
			# Convert to [-180, 180[
			if deg >= 180.0:
				deg = deg - 360.0
			# Convert to radians
			rad = deg * math.pi / 180.0
			return float(rad)

		# TODO: change YAML format and remove /100.0
		self._neutral = neutral / 100.0

		if poly is None or len(poly) ==  0:
			self._phis = np.array([])
			self._dofs = np.array([])
			self._interp_poly = lambda x: self._neutral
		else:
			# The control polygon has one or more DOF values
			phis = map(deg_to_rad_minpi_pluspi, poly.keys())
			dofs = map(lambda x: float(x)/100.0, poly.values()) # TODO: remove /100.0

			# First point in the control polygon.
			# To be appended at the end to simulate looparound behavior
			a_phi = min(phis)
			a_dof = dofs[ phis.index(a_phi) ]

			# Last point in the control polygon.
			# To be prepended at the beginning to simulate looparound behavior
			b_phi = max(phis)
			b_dof = dofs[ phis.index(b_phi) ]

			phis = [b_phi - 2*math.pi] + phis + [a_phi + 2*math.pi]
			dofs = [b_dof] + dofs + [a_dof]

			# Sort lists
			indexes = range(len(phis))
			indexes.sort(key=phis.__getitem__)
			sorted_phis = map(phis.__getitem__, indexes)
			sorted_dofs = map(dofs.__getitem__, indexes)

			# Convert to numpy arrays
			self._phis = np.array(sorted_phis)
			self._dofs = np.array(sorted_dofs)

			# Create interpolation instance
			self._interp_poly = interpolate.interp1d(sorted_phis, sorted_dofs, kind="linear")

	def calc(self, phi, r):
		# Calculate DOF position at max intensity
		dof_at_max_r = self._interp_poly(phi)

		# Interpolate between neutral DOF pos and max intensity DOF pos
		self.cached_pos = self._neutral + (r * (dof_at_max_r - self._neutral))

		# Execute overlays
		for overlay_fn in self.overlays:
			try:
				self.cached_pos = overlay_fn(self.cached_pos, self)
			except TypeError:
				# Not a callable object, or function does not take 2 args
				pass

		return self.cached_pos

	def add_overlay(self, fn):
		self.overlays.append(fn)

	def remove_overlay(self, fn):
		self.overlays.remove(fn)

	def clear_overlays(self):
		self.overlays = []


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
		self.pin = pin
		self.dofname = dofname
		self.min_range = min_range
		self.mid_pos = mid_pos
		self.max_range = max_range

	def __repr__(self):
		return "Servo(pin=%d, min_range=%d, mid_pos=%d, max_range=%d, dofname=%s)" \
		 % (self.pin, self.min_range, self.mid_pos, self.max_range, self.dofname)

	def dof_to_us(self, dof_pos):
		"""Converts DOF pos to microseconds. DOF pos from -1.0 to 1.0."""
		# TODO: is int() necessary? Check later if return value can be float
		if dof_pos >= 0:
			return int(self.mid_pos + dof_pos*self.max_range)
		else:
			return int(self.mid_pos + -dof_pos*self.min_range)

class _Expression(object):
	def __init__(self):
		self._emotion = 0 + 0j
		self._anim = None

		self.servos = []
		self.dofs = {}
		self.dof_values = {}
		self.lock = threading.Lock()

		self.empty_config()
		self.load_config()
		self.isEmotion = False

	def get_emotion_complex(self):
		"""
		Returns current emotion as a complex number
		"""
		return self._emotion

	def set_emotion(self, valence=None, arousal=None, r=None, phi=None, degrees=False, anim_time=0):
		self.isEmotion = True

		# TODO: Phi in deg or radians? Internally probably radians
		e = 0 + 0j
		if valence is not None and arousal is not None:
			e = valence + arousal*1j
		elif r is not None and phi is not None:
			if degrees:
				phi = phi * math.pi/180.0
			e = cmath.rect(r, phi)
		else:
			raise RuntimeError("Bad combination of parameters. Either valence and arousal or r and phi need to be provided.")

		# Make sure emotion is restricted to within unity circle.
		if abs(e) > 1.0:
			e = cmath.rect(1.0, cmath.phase(e))

		if anim_time > 0:
			self._anim = Animate([0, anim_time], [self._emotion, e])
		else:
			self._emotion = e

	def set_emotion_val_ar(self, valence, arousal, anim_time=0):
		self.set_emotion(valence=valence, arousal=arousal, anim_time=anim_time)

	def set_emotion_r_phi(self, r, phi, degrees=False, anim_time=0):
		self.set_emotion(r=r, phi=phi, degrees=degrees, anim_time=anim_time)

	def set_dof_values(self, dof_position_values):
		self.isEmotion = False
		for dof in dof_position_values:
		 	dof_position_values[dof] = constrain(dof_position_values[dof], -1.0, 1.0)
		self.dof_values = dof_position_values

	def update(self):
		if self._anim is not None:
			self._emotion = self._anim()
			if self._anim.has_ended():
				self._anim = None

		phi = cmath.phase(self._emotion)
		r = abs(self._emotion)

		# Create a list of dummy values.
		# None indicates that the servo at that index will not be updated.
		servo_pos_us = [None for i in range(16)]

		# Buffer to store all DOF values
		#self.dof_values = {}

		# (1) Calculate DOF positions using phi/r
		# (2) This step also applies overlay functions to the DOFs
		if self.isEmotion:
			for dofname, dof in self.dofs.iteritems():
				self.dof_values[dofname] = dof.calc(phi, r)

		# (3) Update all servos
		for servo in self.servos:
			if servo.pin < 0 or servo.pin > 15:
				continue # Skip invalid pins
			if servo.dofname in self.dof_values:
				servo_pos_us[servo.pin] = servo.dof_to_us(self.dof_values[servo.dofname])

		# TODO: send values to hardware

		with Hardware.lock:
			Hardware.servo_set_all(servo_pos_us)


	def empty_config(self):
		self.servos = []
		self.dofs = {}

	def load_config(self):
		def open_yaml(filename):
			"""Helper function to load YAML files into a dict."""
			try:
				yaml_dict = None
				with open(filename) as f:
					yaml_dict = yaml.load(f, Loader=Loader)
				return yaml_dict
			except IOError:
				raise RuntimeError("Could not open YAML file: %s" % filename)
		def default(x, e, y):
			"""
			Helper function that attempts to read a key from a dict. If the
			specified exception occurs, a default value is returned.
			"""
			try:
				return x()
			except e:
				return y

		pinmap_yaml = open_yaml(_configs["pinmap"])
		limits_yaml = open_yaml(_configs["limits"])
		functions_yaml = open_yaml(_configs["functions"])

		self.empty_config()

		# Create all Servo objects
		# Starts from pinmap, as a servo needs to have a pin associated with it.
		# If DOF not found in limits, default values are assigned.
		for pin, dofname in pinmap_yaml.iteritems():
			dofname = str(dofname) # Force into str

			s = {}
			s["pin"] = pin
			s["dofname"] = dofname
			s["min_range"] = default(lambda: limits_yaml[dofname]["min"], KeyError, None)
			s["mid_pos"] = default(lambda: limits_yaml[dofname]["mid"], KeyError, None)
			s["max_range"] = default(lambda: limits_yaml[dofname]["max"], KeyError, None)

			# Remove all empty values
			s = {k: v for k, v in s.items() if v is not None}

			# Create new servo object from dict
			self.servos.append(Servo(**s))

		# Create all DOF objects
		# Starts from functions YAML
		# If DOF not found in limits, default values are assigned.
		for dofname, params in functions_yaml.iteritems():
			d = {}
			d["name"] = dofname
			d["neutral"] = default(lambda: params.pop("neutral"), KeyError, None)
			d["poly"] = default(lambda: params.pop("poly"), KeyError, None)

			# Remove all empty values
			d = {k: v for k, v in d.items() if v is not None}

			# Create new DOF object from dict, store extra values from YAML
			dof = DOF(**d)
			dof.data = params
			self.dofs[dofname] = dof

		print_info("Loaded %d DOFs, %d servos" % (len(self.servos), len(self.dofs)) )

# Create singleton-ish Expression instance
Expression = _Expression()
