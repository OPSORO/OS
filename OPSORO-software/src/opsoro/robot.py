import os
from functools import partial
import lupa
from random import randint
import time
import json
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


from opsoro.console_msg import *
from opsoro.stoppable_thread import StoppableThread
from opsoro.hardware import Hardware
from opsoro.Entity.Factory import Factory



class _Robot(object):
    def __init__(self):
        self.entities = {}
        self._config = {}
        self._dof_t = None
        self._alive_t = None

    def start(self):
        print_info('Start Robot')
        with Hardware.lock:
            Hardware.servo_init()
            Hardware.servo_enable()
        self.start_update_loop()

    def start_update_loop(self):
        if self._dof_t is not None:
            self._dof_t.stop()
        self._dof_t = StoppableThread(target=self.dof_update_loop)

    def start_alive_loop(self):
        if self._alive_t is not None:
            self._alive_t.stop()
        self._alive_t = StoppableThread(target=self.alive_loop)

    def stop_alive_loop(self):
        if self._alive_t is not None:
            self._alive_t.stop()

    def stop(self):
        print_info('Stop Robot')
        with Hardware.lock:
            Hardware.servo_disable()

        if self._dof_t is not None:
            self._dof_t.stop()

    def config(self, config=None):
        if config is not None and len(config) > 0:
            self._config = json.loads(config)
            self.entities = Factory(self._config).load_entities()
        return self._config

    def set_dof_value(self, module_name, dof_name, dof_value, anim_time=-1):
        for i in self.entities.values():
            i.set_mod_dof_value(module_name, dof_name, dof_value, anim_time)
        self.start_update_loop()

    # def set_dof_values(self, dof_values, anim_time=-1):
    #     for module_name, dofs in dof_values.iteritems():
    #         for dof_name, dof_value in dofs.iteritems():
    #             self.entities[module_name].set_dof_value(dof_name, dof_value, anim_time)
    #     self.start_update_loop()

    #deprecated
    def get_dof_values(self):
        print_error("use of deprecated method: get_dof_values in robot not supported")
        return None

    def apply_poly(self, r, phi, anim_time=-1):
        # print_info('Apply robot poly; r: %f, phi: %f, time: %f' %
        #            (r, phi, anim_time))
        for name, module in self.entities.iteritems():
            module.apply_poly(r, phi, anim_time)

        self.start_update_loop()

    def dof_update_loop(self):
        time.sleep(0.05)  # delay
        if self._dof_t is None:
            return

        while not self._dof_t.stopped():
            if not self.update():
                self._dof_t.stop()
            self._dof_t.sleep(0.02)

    def alive_loop(self):
        time.sleep(0.05)  # delay
        if self._alive_t is None:
            return
        while not self._alive_t.stopped():
            self._alive_t.sleep(randint(0, 9))

    def update(self):
        updated = False
        for name, module in self.entities.iteritems():
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
        # Save modules to yaml file
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


    #only use in python itself
    def execute(self,action, tags, *args, **kwargs):
        """
            execute function for executing actions on all modules matching
            specific tags.
            comment: Do not call this function from Lua, because the argumens are
            to complicated. Use execute function below

            :param string action:       name of the function in the Entity
            :param list(string) tags:   tags for selecting the modules
            :param *args, **kwargs      extra argumens for function in Entity
        """
        a = locals()
        del a["self"]
        return self.execute(a)

    def execute(self,params):
        """
            execute any action implemented in the selected entity

            :param dict params:     dictionary with the functionname, tags and the arguments
                dict= {
                    "action": "name_of_function_to_execute",
                    "tags": ["tag1","tag2","tag13"],
                    "extra_arg": "value_of_arg",
                    ...
                }
                In Lua:
                    Robot:execute{action="forward",tags={"wheels"},speed=1}
        """
        params = dict(params)

        action = (params["action"] if "action" in params else None)
        tags = (params["tags"] if "tags" in params else [])

        #cast tags from LuaTable to List
        if type(tags).__name__ == '_LuaTable' :
            tags = list(tags.values())
            params["tags"] = tags

        for m in self.get_modules(tags):
            m.execute(params)
        self.start_update_loop()



    def get_modules(self,tags):
        """
            select entities from 'self.entities'

            :param list(string) tags:       list of tags
            :return:                        list of entities
            :rtype:                         List(Entity)
        """
        result = []
        for m in self.entities.values():
            if m.has_tags(tags):
                result = result + [m]

        return result


# Global instance that can be accessed by apps and scripts
Robot = _Robot()
Robot.load_config()
