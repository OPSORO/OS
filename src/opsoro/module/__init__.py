from opsoro.dof.servo import Servo
from opsoro.dof import DOF
from opsoro.console_msg import *

import time

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class Module(object):
    def __init__(self, data=None):
        """
        Module default class. Custom modules should inherit this class and can override functions.

        :param dict data:   configuration data to setup the module
        """
        self.name = ""
        self.position = {}
        self.size = {}
        self.dofs = {}
        # self.servos = []

        if data is not None:
            self.load_module(data)

    def __str__(self):
        return str(self.name)

    def apply_poly(self, r, phi, anim_time=-1):
        """
        Apply poly values r and phi to the module and calculate dof values

        :param float r:         r radius value
        :param float phi:       phi angle value
        :param int anim_time:   animation time in ms
        """
        for name, dof in self.dofs.iteritems():
            dof.calc(r, phi, anim_time)

    def update(self):
        """
        Update all dof values of this module and return if the update changed a dof.

        :return:    True if a dof has been updated
        :rtype:     bool
        """
        # index = 0
        updated = False
        for name, dof in self.dofs.iteritems():
            # dof.update(self.dofs[index].value)
            if dof.update():
                updated = True
        return updated

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        """
        Apply poly values r and phi to the module and calculate dof values

        :param string dof_name:     name of the DOF
        :param string dof_value:    value to set the DOF
        :param int anim_time:       animation time in ms
        """
        if dof_name is None:
            for name, dof in self.dofs.iteritems():
                dof.set_value(dof_value, anim_time)
        else:
            self.dofs[dof_name].set_value(dof_value, anim_time)

    def load_module(self, data):
        """
        Setup modules with given configuration data

        :param dict data:   configuration data to setup the module
        """
        if 'name' in data:
            self.name = data['name']
        else:
            self.name = ""

        self.position = {}
        self.size = {}

        if 'canvas' in data:
            canvas_data = data['canvas']
            self.position['x'] = canvas_data['x']
            self.position['y'] = canvas_data['y']

            self.size['width'] = canvas_data['width']
            self.size['height'] = canvas_data['height']
            self.size['rotation'] = canvas_data['rotation']

        if 'dofs' in data:
            self.dofs = {}
            # self.servos = []
            for dof_data in data['dofs']:
                if 'name' not in dof_data:
                    dof_data['name'] = ""
                #dof_name = self.name + "_" + dof_data['name']
                dof_name = dof_data['name']

                neutral = 0.0
                poly = None
                if 'mapping' in dof_data:
                    mapping_data = dof_data['mapping']
                    if 'neutral' in mapping_data:
                        neutral = mapping_data['neutral']
                    if 'poly' in mapping_data:
                        poly = mapping_data['poly']

                dof = None
                if 'servo' in dof_data:
                    dof = Servo(dof_name, neutral, poly)
                    servo_data = dof_data['servo']
                    if 'pin' in servo_data and 'min' in servo_data and 'mid' in servo_data and 'max' in servo_data:
                        dof.config(servo_data['pin'],
                                   servo_data['min'],
                                   servo_data['mid'],
                                   servo_data['max'], )
                else:
                    dof = DOF(dof_name, neutral, poly)

                self.dofs[dof.name] = dof

    def alive_trigger(self, count_seed=1):
        """
        This is triggered frequently, when the aliveness is turned on.

        :param float count_seed:   seed value for randomization

        :return:    True if the module updated something
        :rtype:     bool
        """
        return False
