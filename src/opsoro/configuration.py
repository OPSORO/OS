"""
This module defines the interface for loading and saving the configuration files of the robot.

.. autoclass:: _Configuration
   :members:
   :undoc-members:
   :show-inheritance:
"""

from __future__ import division
from __future__ import with_statement

import sys
import os
from functools import partial

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

from opsoro.console_msg import *
# from opsoro.stoppable_thread import StoppableThread
# from opsoro.hardware import Hardware
# from opsoro.preferences import Preferences

# Modules
# from opsoro.module import *

class _Configuration(object):
    def __init__(self):
        self.data = {}
        self.load_config()

    def load_config(self):
        """
        Load configuration into data.
        """
        try:
            with open(get_path("config/default.yaml")) as f:
                self.data = yaml.load(f, Loader=Loader)
        except IOError:
            self.data = {}
            print_warning("Could not open config/default.yaml")

        print_info("Configuration loaded")

    def get_module(self, section, item, default):
        """
        Retrieve configuration value.

        :param string section:  category in which the item is defined.
        :param string item:     item to retrieve.
        :param default:         default value to return if the value is not available.

        :return:    preference value
        """
        return self.data.get(section, {}).get(item, default)

    def set(self, section, item, value):
        """
        Set preference value.

        :param string section:  category in which the item is defined.
        :param string item:     item to set.
        :param value:           value to set.
        """
        if value is None:
            return
        try:
            self.data[section][item] = value
        except KeyError:
            self.data[section] = {item: value}

    def save_prefs(self):
        """
        Saves preferences to yaml file.
        """
        try:
            with open(get_path("config/preferences.yaml"), "w") as f:
                f.write(yaml.dump(self.data, default_flow_style=False, Dumper=Dumper))
        except IOError:
            print_warning("Could not save config/preferences.yaml")

    def save(self, filename):
        pass

Configuration = _Configuration()
