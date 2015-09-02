from __future__ import division

from scipy import interpolate
import time

class Animate(object):
	def __init__(self, times, values):
		"""
		Class to facilitate the tweening of values in time. The animation starts
		when the object is created. Once ended, the call method will return the
		last item in values.

		times:  A list of timestamps in seconds, in increasing order. Timestamp
		        0 is the moment the Animate object was created.
		values: A list of numerical values associated with timestamps. First
		        element should be 0.
		"""
		self._start_time = time.time()
		self._end_time = self._start_time + times[-1]

		times_offset = [t + self._start_time for t in times]

		self._iplt = interpolate.interp1d(times_offset, values, kind="linear", bounds_error=False, fill_value=values[-1])

	def __call__(self):
		"""
		Calculates and returns the current value of the animation.
		"""
		# .item() is called so that a values type is returned. Otherwise _iplt
		# returns a 0D numpy array.
		return self._iplt(time.time()).item()

	def has_ended(self):
		"""
		Returns true if the animation has ended.
		"""
		return time.time() > self._end_time

class AnimatePeriodic(object):
	def __init__(self, times, values):
		"""
		Class to facilitate the tweening of values in time. The animation starts
		when the object is created. This class is a variant of the Animate class
		that does not end, but instead repeats its pattern indefinitely.

		times:  A list of timestamps in seconds, in increasing order. timestamp
		        0 is the moment the Animate object was created.
		values: A list of numerical values associated with timestamps. First
		        element should be 0.
		"""
		self._start_time = time.time()
		self._period = times[-1]

		self._iplt = interpolate.interp1d(times, values, kind="linear", bounds_error=False, fill_value=values[-1])

	def __call__(self):
		"""
		Calculates and returns the current value of the animation.
		"""
		t = time.time() - self._start_time
		t = t % self._period
		return self._iplt(t).item()
