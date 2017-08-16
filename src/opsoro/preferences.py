"""
This module defines the interface for communicating with the settings of the robot.

.. autoclass:: _Preferences
   :members:
   :undoc-members:
   :show-inheritance:
"""

from __future__ import division
from __future__ import with_statement

import sys
import os
import subprocess
import re
from functools import partial

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from opsoro.console_msg import *

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))
constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class _Preferences(object):
    def __init__(self):
        """
        Preferences class to store and retrieve settings.
        """
        self.data = {}
        self.load_prefs()

    def load_prefs(self):
        """
        Load preferences into data.
        """
        try:
            with open(get_path("config/preferences.yaml")) as f:
                self.data = yaml.load(f, Loader=Loader)
        except IOError:
            self.data = {}
            print_warning("Could not open config/preferences.yaml")

        print_info("Preferences loaded")

    def get(self, section, item, default):
        """
        Retrieve preference value.

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

    def apply_prefs(self,
                    update_audio=False,
                    update_wireless=False,
                    restart_wireless=False,
                    update_dns=False):
        """
        Apply preferences to the system.

        :param bool update_audio:       True if audio settings have changed and needs to update.
        :param bool update_wireless:    True if wireless settings have changed and the wireless interface needs to update.
        :param bool restart_wireless:   True if wireless settings have changed and the wireless interface needs to restart.
        :param bool update_dns:         True if DNS settings have changed and needs to update.
        """

        def change_conf_setting(txt, name, val):
            pattern = "^%s([ \t]*)=([ \t]*).*$" % name
            new = "%s=%s" % (name, val)
            txt, subs = re.subn(pattern, new, txt, flags=re.MULTILINE)
            if subs == 0:
                if txt[-1:] != "\n":
                    txt = txt + "\n"
                txt = txt + new
            return txt

        FNULL = open(os.devnull, "w")

        if update_audio:
            try:
                vol = self.get("audio", "master_volume", 66)
                vol = constrain(vol, 0, 100)

                subprocess.Popen(
                    ["amixer", "sset", "'Master'", "%d%%" % vol],
                    stdout=FNULL,
                    stderr=subprocess.STDOUT)
            except Exception as e:
                print_error('Preferences: audio could not update.')

        if update_wireless:
            try:
                with open("/etc/hostapd/hostapd.conf", "r+") as f:
                    lines = f.read()

                    ssid = self.get("wireless", "ssid", "OPSORO-bot")
                    password = self.get("wireless", "password", "opsoro123")
                    channel = self.get("wireless", "channel", 6)
                    channel = constrain(int(channel), 1, 11)

                    lines = change_conf_setting(lines, "ssid", ssid)
                    lines = change_conf_setting(lines, "wpa_passphrase", password)
                    lines = change_conf_setting(lines, "channel", channel)

                    f.seek(0)
                    f.write(lines)
                    f.truncate()

                if restart_wireless:
                    subprocess.Popen(
                        ["service", "hostapd", "restart"],
                        stdout=FNULL,
                        stderr=subprocess.STDOUT)
            except Exception as e:
                print_error('Preferences: wifi could not update.')


        if update_dns:
            with open("/etc/dnsmasq.d/dnsmasq.opsoro.conf", "r+") as f:
                lines = f.read()

                # redirect = self.get("wireless", "ssid", "OPSORO-bot")
                # password = self.get("wireless", "password", "opsoro123")
                # channel = self.get("wireless", "channel", 6)
                # channel = constrain(int(channel), 1, 11)

                address = "/play.opsoro.be/192.168.42.1"
                dhcp = "interface:wlan0,192.168.42.100,192.168.42.200,infinite"

                lines = change_conf_setting(lines, "address", address)
                lines = change_conf_setting(lines, "dhcp-range", dhcp)

                f.seek(0)
                f.write(lines)
                f.truncate()
                subprocess.Popen(
                    ["service", "dnsmasq", "restart"],
                    stdout=FNULL,
                    stderr=subprocess.STDOUT)

# Create singleton-ish Preferences instance
Preferences = _Preferences()
