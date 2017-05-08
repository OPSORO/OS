"""
This module defines the interface for communicating with the sound module.

.. autoclass:: _Sound
   :members:
   :undoc-members:
   :show-inheritance:
"""

import glob
import os
import platform
import subprocess
from functools import partial

from opsoro.console_msg import *
from opsoro.sound.tts import TTS
from opsoro.users import Users

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

        self._platform = platform.system()

    def _play(self, filename):
        """
        Play any local file, used internally by other methods

        :param string filename: full filename to play

        """
        FNULL = open(os.devnull, "w")

        if self._platform == "Darwin":
            # OSX playback, used for development
            self.playProcess = subprocess.Popen(
                ["afplay", filename], stdout=FNULL, stderr=subprocess.STDOUT)
        elif not self.jack:
            self.playProcess = subprocess.Popen(
                ["aplay", filename], stdout=FNULL, stderr=subprocess.STDOUT)
        else:
            # self.playProcess = subprocess.Popen(["aplay", "-D", "hw:0,0", full_path], stdout=FNULL, stderr=subprocess.STDOUT)
            self.playProcess = subprocess.Popen(
                ["aplay", "-D", "hw:0,0", filename],
                stdout=FNULL,
                stderr=subprocess.STDOUT)

    def say_tts(self, text, generate_only=False):
        """
        Converts a string to a soundfile using Text-to-Speech libraries

        :param string text:         text to convert to speech
        :param bool generate_only:  do not play the soundfile once it is created
        """
        if text is None:
            return

        full_path = TTS.create(text)

        if generate_only:
            return

        # Send sound to virtual robots
        Users.broadcast_robot({'sound': 'tts', 'msg': text})

        self.stop_sound()
        self._play(full_path)

    def play_file(self, filename):
        """
        Plays an audio file according to the given filename.

        :param string filename:     file to play

        :return:        True if sound is playing.
        :rtype:         bool
        """
        self.stop_sound()
        path = None
        if os.path.splitext(filename)[1] == '':
            filename += '.*'
        for folder in self.sound_folders:
            f = os.path.join(get_path(folder), filename)
            files = glob.glob(f)
            if files:
                path = files[0]
                break

        if path is None:
            print_error("Could not find soundfile \"%s\"." % filename)
            return False

        # Send sound to virtual robots
        name, extension = os.path.splitext(os.path.basename(filename))
        Users.broadcast_robot({'sound': 'file', 'msg': name})

        self._play(path)
        return True

    def get_file(self, filename, tts=False):
        """
        Returns audio file data according to the given filename.

        :param string filename:     file to return the data from

        :return:        Soundfile data.
        :rtype:         var
        """
        path = None
        data = None

        if tts:
            path = TTS.create(filename)
        else:
            if os.path.splitext(filename)[1] == '':
                filename += '.*'
            for folder in self.sound_folders:
                f = os.path.join(get_path(folder), filename)
                files = glob.glob(f)
                if files:
                    path = files[0]
                    break

        if path is None:
            print_error("Could not find soundfile \"%s\"." % filename)
            return data

        try:
            with open(get_path(path)) as f:
                data = f.read()
        except Exception as e:
            print_error(e)

        # Send sound to virtual robots
        return data

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
