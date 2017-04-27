import base64
import glob
import os
import platform
import random
import subprocess
from functools import partial

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_login import current_user, login_user, logout_user
from sockjs.tornado import SockJSConnection, SockJSRouter
from werkzeug.exceptions import default_exceptions

from opsoro.apps import Apps
from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.play import Play
from opsoro.preferences import Preferences
from opsoro.robot import Robot
from opsoro.server.request_handlers.opsoro_data_requests import *
from opsoro.updater import Updater
from opsoro.users import Users, usertypes

try:
    import simplejson as json
except ImportError:
    import json

dof_positions = {}
# Helper function
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


class RHandler(object):
    def __init__(self, server):
        # title
        self.title = "OPSORO play"
        self.robotName = "Robot"

        self.server = server

    def set_urls(self):

        protect = self.server.protected_view

        self.server.flaskapp.add_url_rule("/",                      "index",            protect(self.page_index), )
        self.server.flaskapp.add_url_rule("/login/",                "login",            self.page_login, methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/logout/",               "logout",           self.page_logout, )
        self.server.flaskapp.add_url_rule("/sockjstoken/",          "sockjstoken",      self.page_sockjstoken, )
        self.server.flaskapp.add_url_rule("/shutdown/",             "shutdown",         protect(self.page_shutdown), )
        self.server.flaskapp.add_url_rule("/restart/",              "restart",          protect(self.page_restart), )
        self.server.flaskapp.add_url_rule("/app/close/<appname>/",  "closeapp",         protect(self.page_closeapp), )
        self.server.flaskapp.add_url_rule("/app/open/<appname>/",   "openapp",          protect(self.page_openapp), )

        self.server.flaskapp.add_url_rule("/blockly/",              "blockly",          protect(self.page_blockly), )

        # ----------------------------------------------------------------------
        # DOCUMENTS
        # ----------------------------------------------------------------------
        self.server.flaskapp.add_url_rule("/docs/data/<app_name>/",     "file_data",    protect(docs_file_data),        methods=["GET"], )
        self.server.flaskapp.add_url_rule("/docs/save/<app_name>/",     "file_save",    protect(docs_file_save),        methods=["POST"], )
        self.server.flaskapp.add_url_rule("/docs/delete/<app_name>/",   "file_delete",  protect(docs_file_delete),      methods=["POST"], )
        self.server.flaskapp.add_url_rule("/docs/list/",                "file_list",    protect(self.page_file_list),   methods=["GET"], )

        # ----------------------------------------------------------------------
        # ROBOT
        # ----------------------------------------------------------------------
        self.server.flaskapp.add_url_rule("/robot/",            "robot",            self.page_virtual,          methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/robot/config/",     "robot_config",     protect(robot_config_data), methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/robot/emotion/",    "robot_emotion",    protect(robot_emotion),     methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/robot/dof/",        "robot_dof",        protect(robot_dof_data),    methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/robot/dofs/",       "robot_dofs",       protect(robot_dofs_data),   methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/robot/tts/",        "robot_tts",        protect(robot_tts),         methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/robot/sound/",      "robot_sound",      protect(robot_sound),       methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/robot/servo/",      "robot_servo",      protect(robot_servo),       methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/robot/stop/",       "robot_stop",       protect(robot_stop),        methods=["GET", "POST"], )

        for _exc in default_exceptions:
            self.server.flaskapp.errorhandler(_exc)(self.show_errormessage)

        self.server.flaskapp.context_processor(self.inject_opsoro_vars)

    def render_template(self, template, **kwargs):
        appname = template.split('.')[0]
        kwargs["app"] = {}
        kwargs["title"] = self.title
        kwargs["version"] = random.randint(0, 10000)
        kwargs["online"] = Play.is_online()

        # Set app variables
        if appname in Apps.active_apps:
            app = Apps.apps[appname]
            kwargs["app"]["active"] = True
            kwargs["app"]["name"] = app.config["full_name"].title()
            kwargs["app"]["full_name"] = app.config["full_name"]
            kwargs["app"]["formatted_name"] = app.config["formatted_name"]
            kwargs["app"]["icon"] = app.config["icon"]
            kwargs["app"]["color"] = app.config["color"]
            kwargs["title"] += " - %s" % app.config["full_name"].title()
            kwargs["page_icon"] = app.config["icon"]
            kwargs["page_caption"] = app.config["full_name"]
        else:
            kwargs["app"]["active"] = False

        if 'actions' not in kwargs:
            kwargs['actions'] = {}
        kwargs['actions']['openfile'] = request.args.get("f", None)

        if "closebutton" not in kwargs:
            kwargs["closebutton"] = True

        kwargs["isuser"] = current_user.is_authenticated

        return render_template(template, **kwargs)

    def page_index(self):
        data = {"title": self.title, "index": True, "apps": {}, "active_apps": [], "other_apps": []}

        # if self.server.activeapp in Apps.apps:
        #     app = Apps.apps[self.server.activeapp]
        #     if app.config.has_key('allowed_background'):
        #         if not app.config['allowed_background']:
        #             self.server.stop_current_app()
        #         else:
        #             data["activeapp"] = {"name"             : self.server.activeapp,
        #                                  "full_name"        : app.config["full_name"],
        #                                  "formatted_name"   : app.config["formatted_name"],
        #                                  "icon"             : app.config["icon"],
        #                                  "color"            : app.config['color'],
        #                                  "difficulty"       : app.config['difficulty'],
        #                                  "tags"             : app.config['tags']
        #                                  }

        for appname in sorted(Apps.active_apps):
            app = Apps.apps[appname]
            data["active_apps"].append(app.config["full_name"])

        for appname in sorted(Apps.apps):
            app = Apps.apps[appname]

            if not app.config['categories']:
                data["other_apps"].append({"name": appname,
                                           "full_name": app.config["full_name"],
                                           "formatted_name": app.config["formatted_name"],
                                           "icon": app.config["icon"],
                                           "color": app.config['color'],
                                           "difficulty": app.config['difficulty'],
                                           "tags": app.config['tags'],
                                           "active": (appname in Apps.active_apps),
                                           "connection": app.config['connection'],
                                           })

            for cat in app.config['categories']:
                if cat not in data["apps"]:
                    data["apps"][cat] = []

                data["apps"][cat].append({"name": appname,
                                          "full_name": app.config["full_name"],
                                          "formatted_name": app.config["formatted_name"],
                                          "icon": app.config["icon"],
                                          "color": app.config['color'],
                                          "difficulty": app.config['difficulty'],
                                          "tags": app.config['tags'],
                                          "active": (appname in Apps.active_apps),
                                          "connection": app.config['connection'],
                                          })

        return self.render_template("apps.html", **data)

    def page_login(self):
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        if Play.is_online():
            print_info('ONLINE MODE')
            if request.method == "GET":
                kwargs = {}
                kwargs["title"] = self.title + " - Login"
                kwargs["isbusy"] = False
                kwargs["isuser"] = False
                kwargs["version"] = random.randint(0, 10000)

                return self.render_template("login.html", **kwargs)

            password = request.form["password"]

            if password == Preferences.get("general", "password", default="opsoro123"):
                Users.login_admin()

                # self.server.user_socketrouter.broadcast(self.server.client_sockets, {'action': 'logout'})
                # for e in self.server.client_sockets:
                #     e.broadcast_data('refresh', {})
                #     break

                return redirect(url_for("index"))
            else:
                flash("Wrong password.")
                return redirect(url_for("login"))
        else:
            print_info('OFFLINE MODE')
            login_user(usertypes.Guest())

            return redirect(url_for("index"))

    def page_logout(self):
        Users.logout()

        flash("You have been logged out.")
        return redirect(url_for("login"))

    def page_sockjstoken(self):
        return base64.b64encode(current_user.token)

    def page_shutdown(self):
        if current_user is None or not current_user.is_authenticated or not current_user.is_admin:
            return
        message = ""
        Apps.stop_all()
        Users.broadcast_message('The robot has been shutdown, goodbye!')

        # Run shutdown command with 5 second delay, returns immediately
        if platform.machine() != 'x86_64':
            subprocess.Popen("sleep 5 && sudo halt", shell=True)
        self.server.shutdown()
        return message

    def page_restart(self):
        if current_user is None or not current_user.is_authenticated or not current_user.is_admin:
            return
        message = ""
        Apps.stop_all()
        Users.broadcast_message('The robot is restarting, please reconnect in a couple of seconds.')

        # Run shutdown command with 5 second delay, returns immediately
        if platform.machine() != 'x86_64':
            subprocess.Popen("sleep 5 && sudo reboot", shell=True)
        self.server.shutdown()
        return message

    def page_closeapp(self, appname):
        Apps.stop(appname)
        return redirect(url_for("index"))

    def page_openapp(self, appname):
        if Apps.start(appname):
            return redirect("/apps/%s/" % appname)
        else:
            return redirect(url_for("index"))

    def page_file_list(self):
        data = docs_file_list()
        # page_caption=appSpecificFolderPath
        return self.render_template("_filelist.html", title=self.title + " - Files", page_icon="fa-folder", **data)

    def page_virtual(self):

        # def send_stopped():
        #     Users.send_app_data(config['formatted_name'], "soundStopped", {})

        # if request.method == "POST":
        #     dataOnly = request.form.get("getdata", type=int, default=0)
        #     if dataOnly == 1:
        #         tempDofs = Robot.dof_values()
        #         return json.dumps({'success': True, 'dofs': tempDofs})
        # # 		return Expression.dof_values
        #     frameOnly = request.form.get("frame", type=int, default=0)
        #     if frameOnly == 1:
        #         #return self.render_template("virtual.html", title="Virtual Model", page_caption="Virtual model", page_icon="fa-smile-o", modules=Modules.modules)
        #         pass

        file_location = get_path('../../config/')
        file_name = 'default.conf'
        config_data = ''
        if os.path.isfile(file_location + file_name):
            with open(get_path(file_location + file_name), "r") as f:
                config_data = f.read()
            # config_data = send_from_directory(file_location, file_name)
            # print_info("Default config loaded")

        return self.render_template("virtual.html", title="Virtual Model", page_caption="Virtual model", page_icon="fa-smile-o", modules=Robot.modules, config=config_data)

    def page_blockly(self):
        data = {'soundfiles': [], 'apps_blockly': {}}

        apps_dir = '../../apps/'
        filenames = glob.glob(get_path('../../data/sounds/*.wav'))

        for filename in filenames:
            data['soundfiles'].append(os.path.split(filename)[1])

        for appname in sorted(Apps.apps.keys()):
            app_blockly_path = get_path(apps_dir + appname + '/blockly/')
            if os.path.isdir(app_blockly_path):
                if os.path.exists(app_blockly_path + appname + '.xml') and os.path.exists(app_blockly_path + appname + '.js'):
                    data['apps_blockly'][appname] = {}
                    data['apps_blockly'][appname]['name'] = Apps.apps[appname].config["full_name"]
                    with open(app_blockly_path + appname + '.xml') as f:
                        data['apps_blockly'][appname]['xml'] = f.read()
                    with open(app_blockly_path + appname + '.js') as f:
                        data['apps_blockly'][appname]['js'] = f.read()

        return self.render_template('blockly_template.html', **data)

    def show_errormessage(self, error):
        print_error(error)
        if error.code == 404:
            return redirect("/")
        return ""

    def inject_opsoro_vars(self):
        opsoro = {"robot_name": Preferences.get("general", "robot_name",
                                                self.robotName)}
        return dict(opsoro=opsoro)
