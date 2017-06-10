import os
from functools import partial, wraps

import pluginbase
import yaml
from flask import Blueprint, flash

from opsoro.console_msg import *
from opsoro.robot import Robot
from opsoro.users import Users

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class _Apps(object):
    def __init__(self):
        """
        Apps class.

        """

        # Setup app system
        self.plugin_base = pluginbase.PluginBase(package='opsoro.apps')
        self.plugin_source = self.plugin_base.make_plugin_source(searchpath=[get_path('.')])

        self.apps = {}
        self.active_apps = []
        self.background_apps = []

        # Make sure apps are only registered during setup
        self.apps_can_register_bp = True
        self.current_bp_app = ""            # Keep track of current app for blueprint setup

        Users.app_change_handler = self.refresh_active

        # Socket callback dicts
        # self.sockjs_connect_cb = {}
        # self.sockjs_disconnect_cb = {}

    def start(self, appname):
        if appname in self.active_apps:
            # already activated
            if not self.apps[appname].config['multi_user']:
                flash("This app can only be opened once, and is running elsewhere.")
                return False
        elif appname in self.background_apps:
            self.background_apps.remove(appname)
            self.active_apps.append(appname)
        else:
            if appname in self.apps:
                # robot activation:
                if self.apps[appname].config['activation'] >= Robot.Activation.AUTO:
                    if self.apps[appname].config['activation'] == Robot.Activation.AUTO_NOT_ALIVE:
                        Robot.start(False)
                    else:
                        Robot.start()

                self.active_apps.append(appname)

                try:
                    print_appstarted(appname)
                    self.apps[appname].start(self)
                except AttributeError:
                    print_info("%s has no start function" % appname)

            else:
                return False

        running_apps = []
        running_apps.extend(self.active_apps)
        running_apps.extend(self.background_apps)

        return True

    def stop(self, appname):
        app_count = 0
        for sock in Users.sockets:
            if sock.activeapp == appname:
                app_count += 1

        if app_count > 1:
            return

        if appname in self.active_apps:
            print_appstopped(appname)
            try:
                self.apps[appname].stop(self)
            except AttributeError:
                print_info("%s has no stop function" % appname)
            self.active_apps.remove(appname)

        if len(self.active_apps) < 1:
            Robot.stop()

    def refresh_active(self):
        act_apps = []
        locked_apps = []
        for sock in Users.sockets:
            if sock.activeapp in self.apps:
                act_apps.append(sock.activeapp)

        for app in self.active_apps:
            if app not in act_apps:
                if not self.apps[app].config['allowed_background']:
                    self.stop(app)
                else:
                    self.background_apps.append(app)
                    self.active_apps.remove(app)
            else:
                if not self.apps[app].config['multi_user']:
                    locked_apps.append(app)

        running_apps = []
        running_apps.extend(self.active_apps)
        running_apps.extend(self.background_apps)
        Users.broadcast_data('apps', {'active': running_apps, 'locked': locked_apps})

    def stop_all(self):
        for appname in self.active_apps:
            print_appstopped(appname)
            try:
                self.apps[appname].stop(self)
            except AttributeError:
                print_info("%s has no stop function" % appname)

        self.active_apps = []

        if len(self.active_apps) < 1:
            Robot.stop()

    def register_app_blueprint(self, bp):
        assert self.apps_can_register_bp, "Apps can only register blueprints at setup!"

        prefix = "/apps/" + self.current_bp_app
        self.server.flaskapp.register_blueprint(bp, url_prefix=prefix)

    def app_view(self, f):
        return self.server.app_view(f)

    def app_api(self, f):
        return self.server.app_api(f)

    def render_template(self, template, **kwargs):
        return self.server.render_template(template, **kwargs)

    def app_socket_connected(self, f):
        # appname = f.__module__.split(".")[-1]
        # self.sockjs_connect_cb[appname] = f
        return f

    def app_socket_disconnected(self, f):
        # appname = f.__module__.split(".")[-1]
        # self.sockjs_disconnect_cb[appname] = f
        return f

    def app_socket_message(self, action=""):
        def inner(f):
            appname = f.__module__.split(".")[-1]
            # Create new dict for app if necessary
            if appname not in Users.sockjs_message_cb:
                Users.sockjs_message_cb[appname] = {}
            Users.sockjs_message_cb[appname][action] = f
            return f
        return inner

    def register_apps(self, server):
        self.server = server
        apps_layout = []
        with open(get_path('../config/apps_layout.yaml')) as f:
            apps_layout = yaml.load(f, Loader=Loader)

        for plugin_name in self.plugin_source.list_plugins():
            self.current_bp_app = plugin_name
            plugin = self.plugin_source.load_plugin(plugin_name)
            print_apploaded(plugin_name)

            default_config = {'full_name': 'No name',
                              'formatted_name': 'No_name',
                              'author': 'OPSORO',
                              'icon': 'fa-warning',
                              'color': '#333',
                              'difficulty': 0,
                              'tags': [''],
                              'allowed_background': False,
                              'multi_user': False,
                              'connection': Robot.Connection.OFFLINE,
                              'activation': Robot.Activation.MANUAL}

            if not hasattr(plugin, "config"):
                plugin.config = default_config

            for item in default_config:
                if item not in plugin.config:
                    plugin.config[item] = default_config[item]

            # Add categories for apps-layout
            plugin.config['categories'] = []
            plugin.config['category_index'] = []
            for cat in apps_layout:
                if plugin.config['formatted_name'] in cat['apps']:
                    plugin.config['categories'].append(cat['title'])
                    plugin.config['category_index'].append(cat['apps'].index(plugin.config['formatted_name']))

            self.apps[plugin_name] = plugin
            try:
                plugin.setup(self)
            except AttributeError:
                print_info("%s has no setup function" % plugin_name)

            try:
                plugin.setup_pages(self)
            except AttributeError as e:
                print(e)
                print_info("%s has no setup_pages function" % plugin_name)

        self.current_bp_app = ""
        self.apps_can_register_bp = False
        return self.apps


Apps = _Apps()
