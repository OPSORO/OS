from __future__ import division
from __future__ import with_statement

import math
import cmath
import os
import threading
from functools import partial

import numpy as np
from scipy import interpolate

from opsoro.animate import Animate
from opsoro.hardware import Hardware
from opsoro.hardware.servo import Servo
from opsoro.console_msg import *

from opsoro.modules import Modules

import yaml
try:
    from yaml import CLoader as Loader
    print_info("Using YAML CLoader")
except ImportError:
    print_info(
        "YAML CLoader not available, falling back on python implementation")
    from yaml import Loader

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class _Expression(object):
    def __init__(self):
        self._emotion = 0 + 0j
        self._anim = None

        # self.servos = []
        # self.dofs = {}
        # self.dof_values = {}
        self.lock = threading.Lock()

        # self.empty_config()
        self.load_config()
        # self.isEmotion = False

    def get_emotion_complex(self):
        """
		Returns current emotion as a complex number
		"""
        return self._emotion

    def set_emotion(self,
                    valence=None,
                    arousal=None,
                    r=None,
                    phi=None,
                    degrees=False,
                    anim_time=0):
        print_info("Emotion: " + str(valence) + ", " + str(arousal) + ", " +
                   str(r) + ", " + str(phi) + ", " + str(degrees) + ", " + str(
                       anim_time))
        # self.isEmotion = True

        # TODO: Phi in deg or radians? Internally probably radians
        e = 0 + 0j
        if valence is not None and arousal is not None:
            e = valence + arousal * 1j
        elif r is not None and phi is not None:
            if degrees:
                phi = phi * math.pi / 180.0
            e = cmath.rect(r, phi)
        else:
            raise RuntimeError(
                "Bad combination of parameters. Either valence and arousal or r and phi need to be provided.")

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

    # def set_dof_values(self, dof_position_values):
    # 	self.isEmotion = False
    # 	for dof in dof_position_values:
    # 	 	dof_position_values[dof] = constrain(dof_position_values[dof], -1.0, 1.0)
    # 	self.dof_values = dof_position_values

    def update(self):
        if self._anim is not None:
            self._emotion = self._anim()
            if self._anim.has_ended():
                self._anim = None

        phi = cmath.phase(self._emotion)
        r = abs(self._emotion)

        # if self.isEmotion:
        Modules.apply_poly(phi, r)

        Modules.update()
        return
        #
        #
        # # Create a list of dummy values.
        # # None indicates that the servo at that index will not be updated.
        # servo_pos_us = [None for i in range(16)]
        #
        # # Buffer to store all DOF values
        # #self.dof_values = {}
        #
        # # (1) Calculate DOF positions using phi/r
        # # (2) This step also applies overlay functions to the DOFs
        # if self.isEmotion:
        # 	for dofname, dof in self.dofs.iteritems():
        # 		self.dof_values[dofname] = dof.calc(phi, r)
        #
        # # (3) Update all servos
        # for servo in self.servos:
        # 	if servo.pin < 0 or servo.pin > 15:
        # 		continue # Skip invalid pins
        # 	if servo.dofname in self.dof_values:
        # 		servo_pos_us[servo.pin] = servo.dof_to_us(self.dof_values[servo.dofname])
        #
        # # TODO: send values to hardware
        #
        # with Hardware.lock:
        # 	Hardware.servo_set_all(servo_pos_us)

    # def empty_config(self):
    # 	self.servos = []
    # 	self.dofs = {}
    #

    def load_config(self):
        Modules.load_modules("default.conf")
        return
    #
    #
    # 	def open_yaml(filename):
    # 		"""Helper function to load YAML files into a dict."""
    # 		try:
    # 			yaml_dict = None
    # 			with open(filename) as f:
    # 				yaml_dict = yaml.load(f, Loader=Loader)
    # 			return yaml_dict
    # 		except IOError:
    # 			raise RuntimeError("Could not open YAML file: %s" % filename)
    # 	def default(x, e, y):
    # 		"""
    # 		Helper function that attempts to read a key from a dict. If the
    # 		specified exception occurs, a default value is returned.
    # 		"""
    # 		try:
    # 			return x()
    # 		except e:
    # 			return y
    #
    # 	pinmap_yaml = open_yaml(_configs["pinmap"])
    # 	limits_yaml = open_yaml(_configs["limits"])
    # 	functions_yaml = open_yaml(_configs["functions"])
    #
    # 	self.empty_config()
    #
    # 	# Create all Servo objects
    # 	# Starts from pinmap, as a servo needs to have a pin associated with it.
    # 	# If DOF not found in limits, default values are assigned.
    # 	for pin, dofname in pinmap_yaml.iteritems():
    # 		dofname = str(dofname) # Force into str
    #
    # 		s = {}
    # 		s["pin"] = pin
    # 		s["dofname"] = dofname
    # 		s["min_range"] = default(lambda: limits_yaml[dofname]["min"], KeyError, None)
    # 		s["mid_pos"] = default(lambda: limits_yaml[dofname]["mid"], KeyError, None)
    # 		s["max_range"] = default(lambda: limits_yaml[dofname]["max"], KeyError, None)
    #
    # 		# Remove all empty values
    # 		s = {k: v for k, v in s.items() if v is not None}
    #
    # 		# Create new servo object from dict
    # 		self.servos.append(Servo(**s))
    #
    # 	# Create all DOF objects
    # 	# Starts from functions YAML
    # 	# If DOF not found in limits, default values are assigned.
    # 	for dofname, params in functions_yaml.iteritems():
    # 		d = {}
    # 		d["name"] = dofname
    # 		d["neutral"] = default(lambda: params.pop("neutral"), KeyError, None)
    # 		d["poly"] = default(lambda: params.pop("poly"), KeyError, None)
    #
    # 		# Remove all empty values
    # 		d = {k: v for k, v in d.items() if v is not None}
    #
    # 		# Create new DOF object from dict, store extra values from YAML
    # 		dof = DOF(**d)
    # 		dof.data = params
    # 		self.dofs[dofname] = dof
    #
    # 	print_info("Loaded %d DOFs, %d servos" % (len(self.servos), len(self.dofs)) )

    # Create singleton-ish Expression instance


Expression = _Expression()
