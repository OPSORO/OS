import os
import string
from functools import partial
import subprocess
from preferences import Preferences

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

class _TTS(object):
	def __init__(self):
		self.engine = "espeak" # "espeak"
		self.language = "nl"
		self.gender = "f" # "m"
		self.delay = "5"
		self.speed = "180"

	def create(self, text):
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

		if not os.path.exists("/tmp/OpsoroTTS/"):
			os.makedirs("/tmp/OpsoroTTS/")

		filename = format_filename(text)

		# Max length of filename is 255 chars
		if len(filename) >= 250:
			filename = filename[:250]
		full_path = os.path.join(get_path("/tmp/OpsoroTTS/"), filename + ".wav")

		if os.path.isfile(full_path):
			# Sound file already exists
			return full_path

		self.engine = Preferences.get("audio", "tts_engine", self.engine)
		self.language = Preferences.get("audio", "tts_language", self.language)
		self.gender = Preferences.get("audio", "tts_gender", self.gender)

		if self.engine == "pico":
			self.create_pico(text, full_path)
		elif self.engine == "espeak":
			self.create_espeak(text, full_path, self.language, self.gender, self.delay, self.speed)

		return full_path

	def create_pico(self, text, file_path):
		subprocess.call(["pico2wave", "-w", file_path, text])

	def create_espeak(self, text, file_path, language, gender, delay, speed):
		text = "\"" + text + "\""
		subprocess.call(["espeak", "-v", language + "+" + gender + "3", "-g", delay, "-s", speed, "-w", file_path, text])
# Global instance that can be accessed by apps and scripts
TTS = _TTS()
