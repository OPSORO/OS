"""
This module defines the interface for communicating with the expression.

.. autoclass:: _Expression
   :members:
   :undoc-members:
   :show-inheritance:
"""

from __future__ import with_statement

import math
import os
from functools import partial

import cmath
from opsoro.console_msg import *
from opsoro.robot import Robot

try:
    import simplejson as json
except ImportError:
    import json


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class _Expression(object):
    def __init__(self):
        self._emotion = 0 + 0j
        self._anim = None

        self.expressions = []

        self.load_config()

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
        if valence is None or arousal is None:
            raise RuntimeError("Bad combination of parameters; valence and arousal need to be provided.")

        valence = constrain(valence, -1.0, 1.0)
        arousal = constrain(arousal, -1.0, 1.0)
        e = valence + arousal * 1j

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
        if r is None or phi is None:
            raise RuntimeError("Bad combination of parameters; r and phi need to be provided.")

        if degrees:
            phi = phi * math.pi / 180.0

        phi = constrain(phi, 0.0, 2 * math.pi)
        r = constrain(r, 0.0, 1.0)

        Robot.apply_poly(r, phi, anim_time)

    def update(self):
        # Still here for backwards compatibility
        # This is done automatically
        return

    def get_emotion_complex(self):
        """
        Returns current emotion as a complex number
        """
        return self._emotion

    def set_emotion_name(self, name, anim_time=-1):
        """
        Set an emotion with name if defined in expression list, within a certain time.
        """

        e = 0 + 0j
        # Emotion from name in list
        if name is None:
            raise RuntimeError("Bad combination of parameters; name needs to be provided.")

        index = 0
        for exp in self.expressions:
            if 'name' in exp:
                if exp['name'] == name:
                    self.set_emotion_index(index, anim_time)
            index += 1

    def set_emotion_icon(self, icon, anim_time=-1):
        """
        Set an emotion with icon if defined in expression list, within a certain time.
        """

        e = 0 + 0j
        # Emotion from icon in list
        if icon is None:
            raise RuntimeError("Bad combination of parameters; icon needs to be provided.")

        index = 0
        for exp in self.expressions:
            if 'icon' in exp:
                if exp['icon'] == icon:
                    self.set_emotion_index(index, anim_time)
            index += 1

    def set_emotion_index(self, index, anim_time=-1):
        """
        Set an emotion with index in defined expression list, within a certain time.
        """

        e = 0 + 0j
        # Emotion from list
        if index is None:
            raise RuntimeError("Bad combination of parameters; index needs to be provided.")

        index = constrain(index, 0, len(self.expressions) - 1)

        exp = self.expressions[index]

        if 'poly' in exp:
            # 20 values in poly, (poly * 2*pi/20)
            phi = constrain(exp['poly'] * math.pi / 10, 0.0, 2 * math.pi)
            Robot.apply_poly(1.0, phi, anim_time)

        if 'dofs' in exp:
            # send dofs directly to the robot
            Robot.set_dof_list(exp['dofs'], anim_time)

    def set_config(self, config=None):
        if config is not None and len(config) > 0:
            save_new_config = (self.expressions != config)
            self.expressions = json.loads(config)
            # Create all module-objects from data

            if save_new_config:
                self.save_config()

        return self.expressions

    def load_config(self, file_name='robot_expressions.conf'):
        # Load modules from file
        if file_name is None:
            return False

        try:
            with open(get_path("config/" + file_name)) as f:
                self.expressions = f.read()

            if self.expressions is None or len(self.expressions) == 0:
                print_warning("Config contains no data: " + file_name)
                return False

            self.set_config(self.expressions)
            # print module feedback
            print_info("%i expressions loaded [%s]" % (len(self.expressions), file_name))

        except IOError:
            self.expressions = {}
            print_warning("Could not open " + file_name)
            return False

        return True

    def save_config(self, file_name='robot_expressions.conf'):
        # Save modules to json file
        if file_name is None:
            return False

        try:
            with open(get_path("config/" + file_name), "w") as f:
                f.write(json.dumps(self.expressions))
            print_info("Expressions saved: " + file_name)
        except IOError:
            print_warning("Could not save " + file_name)
            return False
        return True


# Global instance that can be accessed by apps and scripts
Expression = _Expression()
