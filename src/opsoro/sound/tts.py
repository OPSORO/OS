"""
This module defines the interface for communicating with the TTS libraries.

.. autoclass:: _TTS
   :members:
   :undoc-members:
   :show-inheritance:
"""

import hashlib
import os
import string
import subprocess
from functools import partial

from opsoro.preferences import Preferences

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class _TTS(object):
    def __init__(self):
        """
        TTS class, used to convert text to speech.
        """
        self.engine = "espeak"  # "espeak"
        self.language = "nl"
        self.gender = "f"  # "m"
        self.delay = "5"
        self.speed = "180"
        self.cache_folder = "/tmp/opsorotts"

    def create(self, text):
        """
        Takes a string of text, converts it using the PicoTTS engine, and plays it.
        Wave files are buffered in /tmp/OnoTTS/<text>.wav.
        First call blocks while PicoTTS generates the .wav, this may take about a second.
        Subsequent calls of the same text return immediately.
        If you wish to avoid this, sound files can be generated on beforehand by
        using generate_only=True.

        :param string text:         text to convert to speech

        :return:    path to the sound file
        :rtype:     string
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

            :param string s:  text to convert to a valid filename

            :return:    formatted filename
            :rtype:     string
            """
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            filename = ''.join(c for c in s if c in valid_chars)
            filename = filename.replace(
                ' ', '_')  # I don't like spaces in filenames.
            return filename

        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)

        filename = hashlib.sha1(format_filename(text))

        # Max length of filename is 255 chars

        # if len(filename) >= 250:
        #     filename = filename[:250]
        full_path = os.path.join(get_path(self.cache_folder), filename + ".wav")

        if os.path.isfile(full_path):
            # Sound file already exists
            return full_path

        self.engine = Preferences.get("audio", "tts_engine", self.engine)
        self.language = Preferences.get("audio", "tts_language", self.language)
        self.gender = Preferences.get("audio", "tts_gender", self.gender)

        if self.engine == "pico":
            self.create_pico(text, full_path)
        elif self.engine == "espeak":
            self.create_espeak(text, full_path, self.language, self.gender,
                               self.delay, self.speed)

        return full_path

    def create_pico(self, text, file_path):
        """
        Convert text to speech using the pico2wave TTS library.

        :param string text:         text to convert to speech
        :param string file_path:    file path to store the speech soundfile
        """
        subprocess.call(["pico2wave", "-w", file_path, text])

    def create_espeak(self, text, file_path, language, gender, delay, speed):
        """
        Convert text to speech using the espeak TTS library.

        :param string text:         text to convert to speech
        :param string file_path:    file path to store the speech soundfile
        :param string language:     language initials
        :param string gender:       specify gender (m for male, f for female)
        :param int delay:           delay between words in ms
        :param int speed:           speed in words-per-minute
        """
        text = "\"" + text + "\""
        subprocess.call(["espeak", "-v", language + "+" + gender + "3", "-g", delay, "-s", speed, "-w", file_path, text])


# Global instance that can be accessed by apps and scripts
TTS = _TTS()
