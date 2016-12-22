from opsoro.console_msg import *
from opsoro.stoppable_thread import StoppableThread
from opsoro.hardware import Hardware
from opsoro.preferences import Preferences

from functools import partial
import os
import time

try:
    import simplejson as json
except ImportError:
    import json

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

# Modules
from opsoro.module import *
from opsoro.module.eye import Eye
from opsoro.module.eyebrow import Eyebrow
from opsoro.module.mouth import Mouth

MODULES = {'eye': Eye, 'eyebrow': Eyebrow, 'mouth': Mouth}


class _Robot(object):
    def __init__(self):
        self.modules = {}
        self._config = {}
        self.load_config()
        self._dof_t = None
        self._alive_t = None

        self.look_at_position = [0, 0, 0]  # x y z(= depth) -1.0 <-> 1.0

        self.auto_enable_servos = False

        self._alive_count_seed = 1.0
        self._add_seed = 0.2

    def start(self):
        print_info('Start Robot loop')
        with Hardware.lock:
            Hardware.servo_init()
        self.start_update_loop()

        if Preferences.get('alive', 'enabled', False):
            self.start_alive_loop()

    def start_update_loop(self):
        if self._dof_t is not None:
            self._dof_t.stop()

        with Hardware.lock:
            Hardware.servo_enable()

        self._dof_t = StoppableThread(target=self.dof_update_loop)

    def stop_update_loop(self):
        if self._dof_t is not None:
            self._dof_t.stop()

        if self.auto_enable_servos:
            with Hardware.lock:
                Hardware.servo_disable()

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
            Hardware.servo_disable()

        self.stop_alive_loop()
        self.stop_update_loop()

    def config(self, config=None):
        if config is not None and len(config) > 0:
            self._config = json.loads(config)
            # Create all module-objects from data
            self.modules = {}
            modules_count = {}
            for module_data in self._config['modules']:
                if module_data['module'] in MODULES:
                    # Create module object
                    module = MODULES[module_data['module']](module_data)

                    # Count different modules
                    if module_data['module'] not in modules_count:
                        modules_count[module_data['module']] = 0
                    modules_count[module_data['module']] += 1
                    self.modules[module.name] = module

            # print module feedback
            print_info("Modules: " + str(modules_count))
        return self._config

    def set_dof_value(self, module_name, dof_name, dof_value, anim_time=-1):
        if module_name is None:
            for name, module in self.modules.iteritems():
                module.set_dof_value(None, dof_value, anim_time)
        else:
            self.modules[module_name].set_dof_value(dof_name, dof_value,
                                                    anim_time)

        self.start_update_loop()

    def set_dof_values(self, dof_values, anim_time=-1):
        for module_name, dofs in dof_values.iteritems():
            for dof_name, dof_value in dofs.iteritems():
                self.modules[module_name].set_dof_value(dof_name, dof_value,
                                                        anim_time)

        self.start_update_loop()

    def get_dof_values(self):
        dofs = []
        for i in range(16):
            dofs.append(0)
        for module_name, module in self.modules.iteritems():
            for dof_name, dof in module.dofs.iteritems():
                if hasattr(dof, 'pin'):
                    dofs[int(dof.pin)] = float(dof.value)

        return dofs

    def apply_poly(self, r, phi, anim_time=-1):
        # print_info('Apply robot poly; r: %f, phi: %f, time: %f' %
        #            (r, phi, anim_time))
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

    def load_config(self, file_name='default.conf'):
        # Load modules from file
        if file_name is None:
            return False

        try:
            with open(get_path("config/" + file_name)) as f:
                self._config = f.read()

            if self._config is None or len(self._config) == 0:
                print_warning("Config contains no data: " + file_name)
                return False
            # print module feedback
            print_info("Modules loaded [" + file_name + "]")
            self.config(self._config)

        except IOError:
            self._config = {}
            print_warning("Could not open " + file_name)
            return False

        return True

    def save_config(self, file_name='default.conf'):
        # Save modules to json file
        if file_name is None:
            return False

        try:
            with open(get_path("config/" + file_name), "w") as f:
                f.write(json.dumps(self._config))
            print_info("Modules saved: " + file_name)
        except IOError:
            print_warning("Could not save " + file_name)
            return False
        return True

    def blink(self, speed):
        for name, module in self.modules.iteritems():
            if hasattr(module, 'blink'):
                module.blink(speed)

# Global instance that can be accessed by apps and scripts
Robot = _Robot()
