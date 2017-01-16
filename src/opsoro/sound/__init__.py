"""
This module defines the interface for communicating with the sound module.

.. autoclass:: _Sound
   :members:
   :undoc-members:
   :show-inheritance:
"""

from functools import partial
import os
import subprocess
from opsoro.sound.tts import TTS

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class _Sound(object):
    def __init__(self):
        """
        Sound class, used to play sound and speak text.
        """
        # List of search folders for sound files
        self.sound_folders = ["../data/sounds/"]
        self.playProcess = None
        self.jack = False

    def say_tts(self, text, generate_only=False):
        """
        Converts a string to a soundfile using Text-to-Speech libraries

        :param string text:         text to convert to speech
        :param bool generate_only:  do not play the soundfile once it is created
        """
        full_path = TTS.create(text)

        if generate_only:
            return

        FNULL = open(os.devnull, "w")

        self.stop_sound()
        if not self.jack:
            self.playProcess = subprocess.Popen(
                ["aplay", full_path], stdout=FNULL, stderr=subprocess.STDOUT)
        else:
            # self.playProcess = subprocess.Popen(["aplay", "-D", "hw:0,0", full_path], stdout=FNULL, stderr=subprocess.STDOUT)
            self.playProcess = subprocess.Popen(
                ["aplay", "-D", "hw:0,0", full_path],
                stdout=FNULL,
                stderr=subprocess.STDOUT)

    def play_file(self, filename):
        """
        Plays an audio file according to the given filename.

        :param string filename:     file to play
        """
        self.stop_sound()
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
            self.playProcess = subprocess.Popen(
                ["aplay", path], stdout=FNULL, stderr=subprocess.STDOUT)
        else:
            # self.playProcess = subprocess.Popen(["aplay", "-D", "hw:0,0", path], stdout=FNULL, stderr=subprocess.STDOUT)
            self.playProcess = subprocess.Popen(
                ["aplay", "-D", "hw:0,0", path],
                stdout=FNULL,
                stderr=subprocess.STDOUT)

    def stop_sound(self):
        """
        Stop the played sound.
        """
        if self.playProcess == None:
            return

        self.playProcess.terminate()
        self.playProcess = None

    def wait_for_sound(self):
        """
        Wait until the played sound is done.
        """
        if self.playProcess == None:
            return

        self.playProcess.wait()
        self.playProcess = None

# Global instance that can be accessed by apps and scripts
Sound = _Sound()
