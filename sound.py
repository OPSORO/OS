from functools import partial
import os
import glob
import subprocess
import string
from tts import TTS

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

class _Sound(object):
	def __init__(self):
		# List of search folders for sound files
		self.sound_folders = ["data/sounds/soundfiles/"]
		self.playProcess = None
		self.jack = False

	def say_tts(self, text, generate_only=False):
		full_path = TTS.create(text)

		if generate_only:
			return

		FNULL = open(os.devnull, "w")

		self.stop_sound();
		if not self.jack:
			self.playProcess = subprocess.Popen(["aplay", full_path], stdout=FNULL, stderr=subprocess.STDOUT)
		else:
			# self.playProcess = subprocess.Popen(["aplay", "-D", "hw:0,0", full_path], stdout=FNULL, stderr=subprocess.STDOUT)
			self.playProcess = subprocess.Popen(["aplay", "-D", "hw:0,0", full_path], stdout=FNULL, stderr=subprocess.STDOUT)

	def play_file(self, filename):
		self.stop_sound();
		path = None
		for folder in self.sound_folders:
			f = os.path.join(get_path(folder), filename)
			if os.path.isfile(f):
				path = f
				break
		if path is None:
			raise ValueError("Could not find soundfile \"%s\"." % filename)
		FNULL = open(os.devnull, "w")
		if not self.jack:
			self.playProcess = subprocess.Popen(["aplay", path], stdout=FNULL, stderr=subprocess.STDOUT)
		else:
			# self.playProcess = subprocess.Popen(["aplay", "-D", "hw:0,0", path], stdout=FNULL, stderr=subprocess.STDOUT)
			self.playProcess = subprocess.Popen(["aplay", "-D", "hw:0,0", path], stdout=FNULL, stderr=subprocess.STDOUT)

	def stop_sound(self):
		if self.playProcess == None:
			return

		self.playProcess.terminate()
		self.playProcess = None

	def wait_for_sound(self):
		if self.playProcess == None:
			return

		self.playProcess.wait()
		self.playProcess = None

# Global instance that can be accessed by apps and scripts
Sound = _Sound()
