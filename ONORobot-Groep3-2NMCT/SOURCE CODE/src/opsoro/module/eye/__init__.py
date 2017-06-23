import time
from random import randint

from noise import pnoise1

from opsoro.console_msg import *
from opsoro.module import Module
from opsoro.preferences import Preferences


# import math


class Eye(Module):
    # pupil_horizontal
    # pupil_vertical
    # eyelid_closure
    def __init__(self, data=None):
        """
        Eye module class inherits default module class.

        :param dict data:   configuration data to setup the module
        """
        super(Eye, self).__init__(data)
        self.blink_return = False

        self.last_look_position = [0, 0, 0]  # x y z(= depth)

        self.blink_delay = 5000
        self.blink_delay_default = 5000
        self.blink_speed = 400
        self.look_delay = 4000
        self.look_delay_default = 4000
        self.look_speed = 500

    def look(self, x=0, y=0, z=0):
        """
        Look function to make the eye look at some point in space.

        :param float x:   x position / horizontal
        :param float y:   y position / vertical
        :param float z:   z position / depth

        :return:    True if the module updated something
        :rtype:     bool
        """
        # print_info('alive: look')
        # self.last_look_position

        # xdiff = self.last_look_position[0] - self.position['x']
        # ydiff = self.last_look_position[1] - self.position['y']
        # radius = math.sqrt(xdiff * xdiff + ydiff * ydiff)
        # maxRadius = self.size['width']
        # if radius > maxRadius:
        #     radius = maxRadius
        # #
        # angle = math.atan2(ydiff, xdiff)
        # xPosPupil = math.cos(angle) * radius + self.position['x']
        # yPosPupil = math.sin(angle) * radius + self.position['y']

        # print_info(self.last_look_position)
        # print_info(xPosPupil)

        # pupil_horizontal
        # oldDOFvalHOR = float(self.dofs['pupil_horizontal'].value) + 0.01

        # self.last_look_position = Robot.look_at_position

        self.dofs['horizontal'].set_overlay_value(0.0 + self.last_look_position[0], -1)
        #            float(self.look_speed) / 1000.0)

        # pupil_vertical
        # oldDOFvalVER = float(self.dofs['pupil_vertical'].value) + 0.01

        self.dofs['vertical'].set_overlay_value(0.0 + self.last_look_position[1], -1)
        #            float(self.look_speed) / 1000.0)

        # self.look_delay = randint(self.look_delay_default*0.5, self.look_delay_default*1.5)
        return True

    def blink(self, anim_time=0.4):
        """
        Triggers the eye to blink

        :param float anim_time:   animation time to perform the blinking action

        :return:    True if the module updated something
        :rtype:     bool
        """
        # eyelid_closure
        currentTime = int(round(time.time() * 1000))
        if self.blink_return:
            # print_info(currentTime - self.last_blink_time)
            if (currentTime - self.dofs['lid'].last_set_time) > (self.blink_delay + (anim_time * 500)):
                # print_info('alive: blink open: ' + str(self.last_blink_time))
                self.dofs['lid'].reset_overlay(float(anim_time) / 2.0)
                # self.dofs['eyelid_closure'].set_overlay_value(
                #     0.5, float(anim_time) / 2.0)
                self.blink_return = False

                # self.blink_delay = randint(self.blink_delay_default*0.5, self.blink_delay_default*1.5)
                return True
        else:
            # print_info('alive: blink close: ' + str(self.last_blink_time))
            self.dofs['lid'].last_set_time = currentTime - self.blink_delay
            self.dofs['lid'].set_overlay_value(-1.0, float(anim_time) / 2.0, False)
            self.blink_return = True
            return True
        return False

    def alive_trigger(self, count_seed):
        """
        This is triggered frequently, when the aliveness is turned on.

        :param float count_seed:   seed value for randomization

        :return:    True if the module updated something
        :rtype:     bool
        """
        currentTime = int(round(time.time() * 1000))
        updated = False
        if Preferences.get('behaviour', 'blink', False):
            if (currentTime - self.dofs['lid'].last_set_time) > self.blink_delay:
                updated = self.blink(self.blink_speed / 1000.0)

        if Preferences.get('behaviour', 'gaze', False):
            if (currentTime - self.dofs['horizontal'].last_set_time) > self.look_delay:
                # Update random looking position
                # if Robot.look_at_position == self.last_look_position:
                for i in range(len(self.last_look_position)):
                    # Add i to the seed for different x, y, z values
                    self.last_look_position[i] = pnoise1(count_seed + i, 1)
                updated = self.look()

        return updated
