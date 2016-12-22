from opsoro.module import Module
from opsoro.console_msg import *
from opsoro.preferences import Preferences

from noise import pnoise1
import time

# import math


class Eye(Module):
    # pupil_horizontal
    # pupil_vertical
    # eyelid_closure
    def __init__(self, data=None):
        super(Eye, self).__init__(data)
        self.blink_return = False

        self.last_look_position = [0, 0, 0]  # x y z(= depth)

        self.blink_delay = 5000
        self.blink_speed = 400
        self.lookdelay = 4000
        self.look_speed = 500

    def look(self, x=0, y=0, z=0):
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

        self.dofs['pupil_horizontal'].set_overlay_value(
            0.0 + self.last_look_position[0], -1)
        #            float(self.look_speed) / 1000.0)

        # pupil_vertical
        # oldDOFvalVER = float(self.dofs['pupil_vertical'].value) + 0.01

        self.dofs['pupil_vertical'].set_overlay_value(
            0.0 + self.last_look_position[1], -1)
        #            float(self.look_speed) / 1000.0)

        return True

    def blink(self, anim_time):
        # eyelid_closure
        currentTime = int(round(time.time() * 1000))
        if self.blink_return:
            # print_info(currentTime - self.last_blink_time)
            if (currentTime - self.dofs['eyelid_closure'].last_set_time) > (
                    self.blink_delay + (anim_time * 500)):
                # print_info('alive: blink open: ' + str(self.last_blink_time))
                self.dofs['eyelid_closure'].reset_overlay(
                    float(anim_time) / 2.0)
                # self.dofs['eyelid_closure'].set_overlay_value(
                #     0.5, float(anim_time) / 2.0)
                self.blink_return = False
                return True
        else:
            # print_info('alive: blink close: ' + str(self.last_blink_time))
            self.dofs[
                'eyelid_closure'].last_set_time = currentTime - self.blink_delay
            self.dofs['eyelid_closure'].set_overlay_value(
                -1.0, float(anim_time) / 2.0, False)
            self.blink_return = True
            return True
        return False

    def alive_trigger(self, count_seed):
        currentTime = int(round(time.time() * 1000))
        updated = False
        if Preferences.get('alive', 'blink', False):
            if currentTime - self.dofs[
                    'eyelid_closure'].last_set_time > self.blink_delay:
                updated = self.blink(self.blink_speed / 1000.0)

        if Preferences.get('alive', 'gaze', False):
            if currentTime - self.dofs[
                    'pupil_horizontal'].last_set_time > self.lookdelay:
                # Update random looking position
                # if Robot.look_at_position == self.last_look_position:
                for i in range(len(self.last_look_position)):
                    # Add i to the seed for different x, y, z values
                    self.last_look_position[i] = pnoise1(count_seed + i, 1)
                updated = self.look()

        return updated
