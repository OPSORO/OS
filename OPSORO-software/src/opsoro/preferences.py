from __future__ import division
from __future__ import with_statement

import sys
import os
import subprocess
import re
from git import Git, Repo
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
        self.data = {}
        self.load_prefs()
        self.dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', '..')) + '/'
        self.git = Git(self.dir)
        self.repo = Repo(self.dir)

    def get_current_branch(self):
        return self.git.branch().split()[-1]

    def get_remote_branches(self):
        branches = []

        # Get all remote branches (not only local)
        returnvalue = self.git.ls_remote('--heads').split()
        # Strip data
        for i in range(len(returnvalue)):
            if i % 2 != 0:
                # Get only branch name (last value)
                branches.append(returnvalue[i].split("/")[-1])
        return branches

    def check_if_update(self):
        # Update local git data
        self.git.fetch()
        # Retrieve git remote <-> local difference status
        status = self.git.status()
        # easy check to see if local is behind
        if status.find('behind') > 0:
            return True
        return False

    def update(self):
        # Create file to let deamon know it has to update before starting the server
        file = open(self.dir + 'OPSORO-software/update.var', 'w+')

        # restart service
        command = ['/usr/sbin/service', 'opsoro', 'restart']
        #shell=FALSE for sudo to work.
        subprocess.call(command, shell=False)

        # Reboot system
        os.system('/sbin/shutdown -r now')

    def load_prefs(self):
        try:
            with open(get_path("config/preferences.yaml")) as f:
                self.data = yaml.load(f, Loader=Loader)
        except IOError:
            self.data = {}
            print_warning("Could not open config/preferences.yaml")

        print_info("Preferences loaded")

    def get(self, section, item, default):
        return self.data.get(section, {}).get(item, default)

    def set(self, section, item, value):
        try:
            self.data[section][item] = value
        except KeyError:
            self.data[section] = {item: value}

    def save_prefs(self):
        try:
            with open(get_path("config/preferences.yaml"), "w") as f:
                f.write(
                    yaml.dump(
                        self.data, default_flow_style=False, Dumper=Dumper))
        except IOError:
            print_warning("Could not save config/preferences.yaml")

    def apply_prefs(self,
                    update_audio=False,
                    update_wireless=False,
                    restart_wireless=False,
                    update_dns=False):
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
            vol = self.get("audio", "master_volume", 66)
            vol = constrain(vol, 0, 100)

            subprocess.Popen(
                ["amixer", "sset", "'Master'", "%d%%" % vol],
                stdout=FNULL,
                stderr=subprocess.STDOUT)

        if update_wireless:
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
