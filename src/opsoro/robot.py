"""
This module defines the interface for communicating with the robot.

.. autoclass:: _Robot
   :members:
   :undoc-members:
   :show-inheritance:
"""


import os
import time
from functools import partial

from enum import IntEnum
from flask_login import current_user

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.module import *
from opsoro.module.eye import Eye
from opsoro.module.mouth import Mouth
from opsoro.module.turn import Turn
from opsoro.preferences import Preferences
from opsoro.stoppable_thread import StoppableThread
from opsoro.users import Users

try:
    import simplejson as json
except ImportError:
    import json


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


MODULES = {'eye': Eye, 'turn': Turn, 'mouth': Mouth}


class _Robot(object):
    class Activation(IntEnum):
        MANUAL = 0     # 0: Manual start/stop
        AUTO = 1     # 1: Start robot automatically (alive feature according to preferences)
        AUTO_ALIVE = 2     # 2: Start robot automatically and enable alive feature
        AUTO_NOT_ALIVE = 3     # 3: Start robot automatically and disable alive feature

    class Connection(IntEnum):
        OFFLINE = 0         # 0: No online capability
        PARTLY = 1         # 1: Needs online for extras, but works without
        ONLINE = 2         # 2: Requires to be online to work

    def __init__(self):
        self.modules = {}
        self.config = {}
        self.load_config()
        self._dof_t = None
        self._alive_t = None

        self.look_at_position = [0, 0, 0]  # x y z(= depth) -1.0 <-> 1.0

        self.auto_enable_servos = False

        self._alive_count_seed = 1.0
        self._add_seed = 0.2

    def start(self, alive=True):
        print_info('Start Robot loop')
        with Hardware.lock:
            Hardware.Servo.init()
        self.start_update_loop()

        if alive:
            if Preferences.get('behaviour', 'enabled', False):
                self.start_alive_loop()

    def start_update_loop(self):
        Users.broadcast_robot({'dofs': self.get_dof_values(False)}, True)

        if self._dof_t is not None:
            self._dof_t.stop()

        with Hardware.lock:
            Hardware.Servo.enable()

        self._dof_t = StoppableThread(target=self.dof_update_loop)

    def stop_update_loop(self):
        if self._dof_t is not None:
            self._dof_t.stop()

        if self.auto_enable_servos:
            with Hardware.lock:
                Hardware.Servo.disable()

    def start_alive_loop(self):
        if self._alive_t is not None:
            self._alive_t.stop()
        self._alive_t = StoppableThread(target=self.alive_loop)

    def stop_alive_loop(self):
        if self._alive_t is not None:
            self._alive_t.stop()

    def stop(self):
        print_info('Stop Robot loop')

        with Hardware.lock:
            Hardware.Servo.disable()

        self.stop_alive_loop()
        self.stop_update_loop()

    def set_config(self, config=None):
        if config is not None and len(config) > 0:
            save_new_config = (self.config != config)
            self.config = json.loads(config)
            # Create all module-objects from data
            self.modules = {}
            modules_count = {}
            for module_data in self.config['modules']:
                module_type = module_data['type']
                if module_type in MODULES:
                    # Create module object
                    module = MODULES[module_type](module_data)

                    # Count different modules
                    if module_type not in modules_count:
                        modules_count[module_type] = 0
                    modules_count[module_type] += 1

                    if module.name in self.modules:
                        for i in range(1000):
                            if ('%s %i' % (module.name, i)) not in self.modules:
                                module.name = ('%s %i' % (module.name, i))
                                break

                    self.modules[module.name] = module

            # print module feedback
            print_info("Modules: " + str(modules_count))

            if save_new_config:
                self.save_config()
            Users.broadcast_robot({'refresh': True})
        return self.config

    def set_dof(self, tags=[], value=0, anim_time=-1):
        for name, module in self.modules.iteritems():
            module.set_dof(tags, value, anim_time)
        self.start_update_loop()

    def set_dof_value(self, module_name, dof_name, dof_value, anim_time=-1):
        if module_name is None:
            for name, module in self.modules.iteritems():
                module.set_dof_value(None, dof_value, anim_time)
        else:
            self.modules[module_name].set_dof_value(dof_name, dof_value, anim_time)

        self.start_update_loop()

    def set_dof_values(self, dof_values, anim_time=-1):
        for module_name, dofs in dof_values.iteritems():
            for dof_name, dof_value in dofs.iteritems():
                self.modules[module_name].set_dof_value(dof_name, dof_value, anim_time)

        self.start_update_loop()

    def set_dof_list(self, dof_values, anim_time=-1):
        for name, module in self.modules.iteritems():
            for name, dof in module.dofs.iteritems():
                if hasattr(dof, 'pin') and dof.pin is not None:
                    if dof.pin >= 0 and dof.pin < len(dof_values):
                        dof.set_value(dof_values[dof.pin], anim_time)

        self.start_update_loop()

    def get_dof_values(self, current=True):
        dofs = []
        for i in range(16):
            dofs.append(0)
        for module_name, module in self.modules.iteritems():
            for dof_name, dof in module.dofs.iteritems():
                if hasattr(dof, 'pin') and dof.pin is not None:
                    if dof.pin >= 0 and dof.pin < len(dofs):
                        if current:
                            dofs[dof.pin] = float(dof.value)
                        else:
                            dofs[dof.pin] = float(dof.to_value)

        return dofs

    def apply_poly(self, r, phi, anim_time=-1):
        for name, module in self.modules.iteritems():
            module.apply_poly(r, phi, anim_time)

        self.start_update_loop()

    def dof_update_loop(self):
        time.sleep(0.05)  # delay
        if self._dof_t is None:
            return

        while not self._dof_t.stopped():
            if not self.update():
                self.stop_update_loop()
            self._dof_t.sleep(0.02)

    def alive_loop(self):
        time.sleep(0.5)  # delay
        if self._alive_t is None:
            return

        while not self._alive_t.stopped():
            updated = False
            for name, module in self.modules.iteritems():
                if module.alive_trigger(self._alive_count_seed):
                    updated = True
            if updated:
                self._alive_count_seed += self._add_seed
                self.start_update_loop()

            self._alive_t.sleep(0.1)

    def update(self):
        updated = False
        for name, module in self.modules.iteritems():
            if module.update():
                updated = True

        return updated

    def load_config(self, file_name='robot_config.conf'):
        # Load modules from file
        if file_name is None:
            return False

        try:
            with open(get_path("config/" + file_name)) as f:
                self.config = f.read()

            if self.config is None or len(self.config) == 0:
                print_warning("Config contains no data: " + file_name)
                return False

            self.set_config(self.config)
            # print module feedback
            print_info("%i modules loaded [%s]" % (len(self.modules), file_name))

        except IOError:
            self.config = {}
            print_warning("Could not open " + file_name)
            return False

        return True

    def save_config(self, file_name='robot_config.conf'):
        # Save modules to json file
        if file_name is None:
            return False

        try:
            with open(get_path("config/" + file_name), "w") as f:
                f.write(json.dumps(self.config))
            print_info("Modules saved: " + file_name)
        except IOError:
            print_warning("Could not save " + file_name)
            return False
        return True

    def blink(self, speed):
        for name, module in self.modules.iteritems():
            if hasattr(module, 'blink'):
                module.blink(speed)

    def sleep(self):
        print_info('Night night... ZZZZzzzz....')
        self.set_dof(['eye', 'lid'], -1)
        pass

    def wake(self):
        print_info('I am awake!')
        self.set_dof(['eye', 'lid'], 1)
        pass


# Global instance that can be accessed by apps and scripts
Robot = _Robot()
