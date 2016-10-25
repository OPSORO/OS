# from __future__ import division
from __future__ import with_statement

import math
import cmath
# import os
# import threading
# from functools import partial

import numpy as np
from scipy import interpolate

from opsoro.animate import Animate
# from opsoro.hardware import Hardware
# from opsoro.hardware.servo import Servo
from opsoro.console_msg import *

# from opsoro.modules import Modules
from opsoro.robot import Robot

import yaml
try:
    from yaml import CLoader as Loader
    print_info("Using YAML CLoader")
except ImportError:
    print_info(
        "YAML CLoader not available, falling back on python implementation")
    from yaml import Loader

# get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class _Expression(object):
    def __init__(self):
        self._emotion = 0 + 0j
        self._anim = None

    def set_emotion_e(self, e=0 + 0j, anim_time=-1):
        """
		Set an emotion with complex number e, within a certain time.
		"""
        # Print data to log
        # print_info("Emotion; e: " + str(e) + ", time: " + str(anim_time))

        # Make sure emotion is restricted to within unity circle.
        if abs(e) > 1.0:
            e = cmath.rect(1.0, cmath.phase(e))

        # # Apply transition animation
        # if anim_time != 0:
        #     # Set animation-time according to distance between new and previous emotion
        #     if anim_time < 0:
        #         anim_time = abs(e - self._emotion)
        #     self._anim = Animate([0, anim_time], [self._emotion, e])
        # else:
        #     # Set new emotion instantly
        #     self._emotion = e
        self._emotion = e

        phi = cmath.phase(self._emotion)
        r = abs(self._emotion)

        print_info("Set Emotion; r: " + str(r) + ", phi: " + str(phi) +
                   ", time: " + str(anim_time))

        Robot.apply_poly(r, phi, anim_time)

    def set_emotion_val_ar(self, valence, arousal, anim_time=-1):
        """
		Set an emotion with valence and arousal, within a certain time.
		"""
        # Print data to log
        # print_info("Set Emotion; valence: " + str(valence) + ", arousal: " +
        #            str(arousal) + ", time: " + str(anim_time))

        e = 0 + 0j
        # Emotion from valence and arousal
        if valence is not None and arousal is not None:
            valence = constrain(valence, -1.0, 1.0)
            arousal = constrain(arousal, -1.0, 1.0)
            e = valence + arousal * 1j
        else:
            raise RuntimeError(
                "Bad combination of parameters; valence and arousal need to be provided.")
        self.set_emotion_e(e, anim_time)

    def set_emotion_r_phi(self, r, phi, degrees=False, anim_time=-1):
        """
		Set an emotion with r and phi, within a certain time.
		"""
        # Print data to log
        # print_info("Set Emotion; r: " + str(r) + ", phi: " + str(phi) +
        #            ", deg: " + str(degrees) + ", time: " + str(anim_time))

        e = 0 + 0j
        # Emotion from r and phi
        if r is not None and phi is not None:
            if degrees:
                phi = phi * math.pi / 180.0

            phi = constrain(phi, 0.0, 2 * math.pi)
            r = constrain(r, 0.0, 1.0)
            e = cmath.rect(r, phi)
        else:
            raise RuntimeError(
                "Bad combination of parameters; r and phi need to be provided.")

        self.set_emotion_e(e, anim_time)

    def update(self):
        # if self._anim is not None:
        #     self._emotion = self._anim()
        #     if self._anim.has_ended():
        #         self._anim = None
        #
        # phi = cmath.phase(self._emotion)
        # r = abs(self._emotion)
        #
        # Robot.apply_poly(r, phi)
        # Robot.update()

        # This is done automatically
        return

    def get_emotion_complex(self):
        """
		Returns current emotion as a complex number
		"""
        return self._emotion

# def empty_config(self):
# 	self.servos = []
# 	self.dofs = {}
#

# Global instance that can be accessed by apps and scripts
Expression = _Expression()
