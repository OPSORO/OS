from functools import partial
import os
import glob
import subprocess
import string

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

class _Sound(object):
	def __init__(self):
		# List of search folders for sound files
		self.sound_folders = ["apps/sounds/soundfiles/"]

	def say_tts(self, text, generate_only=False):
		"""
		Takes a string of text, converts it using the PicoTTS engine, and plays it.
		Wave files are buffered in /tmp/OnoTTS/<text>.wav.
		First call blocks while PicoTTS generates the .wav, this may take about a second.
		Subsequent calls of the same text return immediately.
		If you wish to avoid this, sound files can be generated on beforehand by
		using generate_only=True.
		"""
		def format_filename(s):
			"""
			Take a string and return a valid filename constructed from the string.
			Uses a whitelist approach: any characters not present in valid_chars are
			removed. Also spaces are replaced with underscores.

			Note: this method may produce invalid filenames such as ``, `.` or `..`
			When I use this method I prepend a date string like '2009_01_15_19_46_32_'
			and append a file extension like '.txt', so I avoid the potential of using
			an invalid filename.

			Taken from: https://gist.github.com/seanh/93666
			"""
			valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
			filename = ''.join(c for c in s if c in valid_chars)
			filename = filename.replace(' ','_') # I don't like spaces in filenames.
			return filename

		FNULL = open(os.devnull, "w")

		if not os.path.exists("/tmp/OnoTTS/"):
			os.makedirs("/tmp/OnoTTS/")

		filename = format_filename(text)

		# Max length of filename is 255 chars
		if len(filename) >= 250:
			filename = filename[:250]
		full_path = os.path.join(get_path("/tmp/OnoTTS/"), filename + ".wav")

		if os.path.isfile(full_path):
			# Sound file already exists, play it
			if generate_only:
				return
			subprocess.Popen(["aplay", full_path], stdout=FNULL, stderr=subprocess.STDOUT)
		else:
			# Sound file does not exist yet, generate it and then play it
			if generate_only:
				subprocess.Popen(["pico2wave", "-w", full_path, text])
			else:
				subprocess.call(["pico2wave", "-w", full_path, text]) # Waits for process to return
				subprocess.Popen(["aplay", full_path], stdout=FNULL, stderr=subprocess.STDOUT)

	def play_file(self, filename):
		path = None
		for folder in self.sound_folders:
			f = os.path.join(get_path(folder), filename)
			if os.path.isfile(f):
				path = f
				break
		if path is None:
			raise ValueError("Could not find soundfile \"%s\"." % filename)
		FNULL = open(os.devnull, "w")
		subprocess.Popen(["aplay", path], stdout=FNULL, stderr=subprocess.STDOUT)

# Global instance that can be accessed by apps and scripts
Sound = _Sound()
