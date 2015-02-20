from __future__ import division
from __future__ import with_statement

from functools import partial
from exceptions import RuntimeError
import os
import math
import yaml
try:
	from yaml import CLoader as Loader
	print "Using YAML CLoader"
except ImportError:
	print "YAML CLoader not available"
	from yaml import Loader

from dof import DOF, EyeHorDOF, EyeVerDOF, MapDOF

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

class ExpressionManager(object):
	def __init__(self, hw, pinmap="pinmap.yaml", limits="limits.yaml", functions="functions.yaml"):
		self.eye_hor = 0
		self.eye_ver = 0
		self.parse_configs(pinmap, limits, functions)
		self.hw = hw

	def parse_configs(self, pinmap="pinmap.yaml", limits="limits.yaml", functions="functions.yaml"):
		# Reset pin map and DOFs
		self.pinmap = [None for i in range(16)] # Initialize with 16 elements to allow random access
		self.dof = {}

		# Parse pin map: pin --> channel name
		try:
			with open(get_path("config/%s" % pinmap)) as f:
				pinmap_yaml = yaml.load(f, Loader=Loader)
				for key in pinmap_yaml:
					try:
						self.pinmap[key] = pinmap_yaml[key]
					except IndexError:
						raise RuntimeError("Invalid pinname in pinmap: %s" % key)
		except IOError:
			raise RuntimeError("Could not open pinmap file: %s" % pinmap)

		# Parse limits: channel name --> limits
		try:
			with open(get_path("config/%s" % limits)) as f:
				limits_yaml = yaml.load(f, Loader=Loader)
		except IOError:
			raise RuntimeError("Could not open limits file: %s" % limits)

		# Parse functions: channel name --> functions
		try:
			with open(get_path("config/%s" % functions)) as f:
				functions_yaml = yaml.load(f, Loader=Loader)
		except IOError:
			raise RuntimeError("Could not open functions file: %s" % functions)

		# Create DOF objects
		for channel_name in self.pinmap:
			if channel_name is not None:
				# Figure out correct DOF class
				try:
					mid_pos = limits_yaml[channel_name]["mid"]
					min_range = limits_yaml[channel_name]["min"]
					max_range = limits_yaml[channel_name]["max"]
				except KeyError:
					raise RuntimeError("Could not find limits for channel %s" % channel_name)

				if "function" in functions_yaml[channel_name]:
					# Function is defined
					function = functions_yaml[channel_name]["function"]
					if function == "manual":
						self.dof[channel_name] = DOF(self, mid_pos, min_range, max_range)
					elif function == "eye_hor":
						self.dof[channel_name] = EyeHorDOF(self, mid_pos, min_range, max_range)
					elif function == "eye_ver":
						self.dof[channel_name] = EyeVerDOF(self, mid_pos, min_range, max_range)
					elif function == "map":
						try:
							neutral = functions_yaml[channel_name]["neutral"]
							poly = functions_yaml[channel_name]["poly"]
						except KeyError:
							raise RuntimeError("Could not parse mapping parameters of channel %s" % channel_name)
						self.dof[channel_name] = MapDOF(self, neutral, poly, mid_pos, min_range, max_range)
					else:
						self.dof[channel_name] = DOF(self, mid_pos, min_range, max_range)
				else:
					# No function defined, use base DOF class
					self.dof[channel_name] = DOF(self, mid_pos, min_range, max_range)

	def set_eyes(self, hor=0, ver=0, steps=0):
		len = math.sqrt(hor*hor + ver*ver)

		if len > 100:
			self.eye_hor = hor*(100/len)
			self.eye_ver = ver*(100/len)
		else:
			self.eye_hor = hor
			self.eye_ver = ver

		for i in range(16):
			name = self.pinmap[i]
			if name is not None:
				try:
					self.dof[name].set_target_eye(steps)
				except AttributeError:
					# DOF is not EyeHorDOF or EyeVerDOF
					pass

	def get_dof_list(self, which=None):
		dof_list = []

		if which == None:
			# Return all DOFs
			for i in range(16):
				name = self.pinmap[i]
				if name is not None:
					dof_list.append(name)
			return dof_list
		elif isinstance(which, int):
			# Return channel name from pin
			if which < 0 or which > 15:
				# Return empty list
				return dof_list

			name = self.pinmap[which]
			if name is not None:
				dof_list.append(name)
			return dof_list
		elif isinstance(which, basestring):
			if which in self.dof:
				dof_list.append(which)
			return dof_list
		elif isinstance(which, list):
			# Return array of channels
			for a in which:
				if isinstance(a, int):
					# Lookup pin
					if a >= 0 and a <= 15:
						name = self.pinmap[a]
						if name is not None:
							dof_list.append(name)
				else:
					# Lookup channel
					if a in self.dof:
						dof_list.append(a)
			return dof_list
		return None;

	def set_target_pos(self, pos, steps=0, which=None):
		dof_list = self.get_dof_list(which)
		if dof_list is None:
			return
		for dofname in dof_list:
			try:
				self.dof[dofname].set_target_pos(pos, steps)
			except AttributeError:
				pass

	def set_target_alpha_length(self, alpha, length, steps=0, which=None):
		dof_list = self.get_dof_list(which)
		if dof_list is None:
			return
		for dofname in dof_list:
			try:
				self.dof[dofname].set_target_alpha_length(alpha, length, steps)
			except AttributeError:
				pass

	def set_target_valence_arousal(self, valence, arousal, steps=0, which=None):
		dof_list = self.get_dof_list(which)
		if dof_list is None:
			return
		for dofname in dof_list:
			try:
				self.dof[dofname].set_target_valence_arousal(valence, arousal, steps)
			except AttributeError:
				pass

	def step(self):
		#print "self.dofs =", self.dof.keys()
		for i in range(16):
			name = self.pinmap[i]
			if name is not None:
				self.dof[name].step()

	def update_servos(self):
		for i in range(16):
			name = self.pinmap[i]
			if name is not None:
				self.hw.set_servo_us(i, int(self.dof[name]))
			else:
				self.hw.set_servo_us(i, 1500)

	def all_servos_min(self):
		for i in range(16):
			name = self.pinmap[i]
			if name is not None:
				self.hw.set_servo_us(i, self.dof[name].min())
			else:
				self.hw.set_servo_us(i, 1500)

	def all_servos_mid(self):
		for i in range(16):
			name = self.pinmap[i]
			if name is not None:
				self.hw.set_servo_us(i, self.dof[name].mid())
			else:
				self.hw.set_servo_us(i, 1500)

	def all_servos_max(self):
		for i in range(16):
			name = self.pinmap[i]
			if name is not None:
				self.hw.set_servo_us(i, self.dof[name].max())
			else:
				self.hw.set_servo_us(i, 1500)


#if __name__ == "__main__":
	#em = ExpressionManager()

	#name = em.pinmap[0]

	#print "tweening", name, "from pos=0 to pos=100 in 20 steps"

	#dof = em.dof[name]
	#em.set_target_pos(pos=100, steps=20, which=None)
	#em.set_target_valence_arousal(valence=0.5, arousal=-0.5, steps=20, which=None)
	#em.set_target_alpha_length(alpha=30, length=0.75, steps=20, which=None)

	#for i in range(30):
	#	em.step()
	#	print i, "->", int(dof), dof.pos_current
	#em.update_servos()
	#print "set eyes"
	#em.set_eyes(0, 50, steps=10)

	#print "all dofs"
	#print em.get_dof_list()
	#print "-----------------"

	#print "one dof by number"
	#print em.get_dof_list(5)
	#print "-----------------"

	#print "one dof by name"
	#print em.get_dof_list("r_eb_inner")
	#print "-----------------"

	#print "multiple dofs by number"
	#print em.get_dof_list([3, 5, 13])
	#print "-----------------"

	#print "multiple dofs by name"
	#print em.get_dof_list(["r_eb_inner", "r_eb_outer", "m_l"])
	#print "-----------------"

	#print "multiple dofs mixed"
	#print em.get_dof_list(["r_eb_inner", 5, "m_l"])
	#print "-----------------"


	#print "--------"
	#dof.set_target_pos(pos=50, steps=10)

	#for i in range(5):
	#	dof.step()
	#	print i, "->", int(dof), dof.pos_current
	#print "--------"
	#dof.set_target_pos(pos=-100, steps=20)
	#for i in range(20):
	#	dof.step()
	#	print i, "->", int(dof), dof.pos_current


	#print em.pinmap
	#print("IDX\tNAME        \tMIN\tMID\tMAX\tFUNCTION")
	#for i in range(16):
	#	name = em.pinmap[i]

	#	if name is not None:
	#		min_ = em.dof[name].min()
	#		mid = em.dof[name].mid()
	#		max_ = em.dof[name].max()
	#		function = em.dof[name].__class__.__name__
	#	else:
	#		min_ = 0
	#		mid = 0
	#		max_ = 0
	#		function = ""
	#	print("%d\t%12s\t%d\t%d\t%d\t%s" % (i, name, min_, mid, max_, function))

	#name = em.pinmap[0]
	#print "poly for ", name
	#print "ALPHA\tPOS"
	#for alpha in range(360):
	#	print "%d\t%.2f" % (alpha, em.dof[name].alpha_to_pos(alpha))
