import threading
import time

class StoppableThread(threading.Thread):
	"""
	Thread class with a stop() method. The thread itself has to check regularly
	for the stopped() condition.
	"""

	def __init__(self, *args, **kwargs):
		super(StoppableThread, self).__init__(*args, **kwargs)
		self._stop = threading.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

	def sleep(self, secs):
		if self.stopped():
			return

		remaining = secs
		delta = 0.2

		# Sleep in intervals of delta
		while remaining > delta:
			time.sleep(delta)
			remaining -= delta
			# Return immediately if stopped
			if self.stopped():
				return

		# Sleep remaining time and return
		time.sleep(remaining)
