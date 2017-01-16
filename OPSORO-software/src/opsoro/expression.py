from __future__ import with_statement

import math
import cmath

from opsoro.console_msg import *

from opsoro.robot import Robot

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


        # Emotion from r and phi
        if r is not None and phi is not None:
            if degrees:
                phi = phi * math.pi / 180.0

            phi = constrain(phi, 0.0, 2 * math.pi)
            r = constrain(r, 0.0, 1.0)
            Robot.apply_poly(r, phi, anim_time)
        else:
            raise RuntimeError(
                "Bad combination of parameters; r and phi need to be provided.")



    def update(self):
        # Still here for backwards compatibility
        # This is done automatically
        return


    def get_emotion_complex(self):
        """
		Returns current emotion as a complex number
		"""
        return self._emotion

# Global instance that can be accessed by apps and scripts
Expression = _Expression()
