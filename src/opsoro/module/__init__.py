import time

from opsoro.console_msg import *
from opsoro.dof import DOF
from opsoro.dof.servo import Servo


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


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

    def set_dof_value(self, dof_name, value, anim_time=-1):
        """
        Set the value of a dof with the given name. If no name is provided, all dofs are set with the given value.

        :param string dof_name:     name of the DOF
        :param float value:         value to set the DOF
        :param int anim_time:       animation time in ms
        """
        if dof_name is None:
            for name, dof in self.dofs.iteritems():
                dof.set_value(value, anim_time)
        else:
            self.dofs[dof_name].set_value(value, anim_time)

    def set_dof(self, tags=[], value=0, anim_time=-1):
        """
        Set the value of a dof with the given tags. If no tags are provided, all dofs are set with the given value.

        :param list tags:           name of the DOF
        :param float value:         value to set the DOF
        :param int anim_time:       animation time in ms
        """
        if type(tags) is not type([]):
            try:
                tags = tags.split(' ')
            except Exception as e:
                print_warning('Unknow tag format. Unable to split unicode.')

        for name, dof in self.dofs.iteritems():
            all_tags = True
            for tag in tags:
                if tag not in dof.tags:
                    all_tags = False
                    break

            if all_tags:
                dof.set_value(value, anim_time)

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

        if 'grid' in data:
            canvas_data = data['grid']
            self.position['x'] = canvas_data['x']
            self.position['y'] = canvas_data['y']
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
                if 'poly' in dof_data:
                    poly = dof_data['poly']

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

                # Add type and name as tags
                dof.tags.extend(data['type'].split(' '))
                dof.tags.extend(self.name.split(' '))
                dof.tags.extend(dof_name.split(' '))

                self.dofs[dof.name] = dof

    def alive_trigger(self, count_seed=1):
        """
        This is triggered frequently, when the aliveness is turned on.

        :param float count_seed:   seed value for randomization

        :return:    True if the module updated something
        :rtype:     bool
        """
        return False
