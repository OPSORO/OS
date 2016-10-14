from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.exceptions import default_exceptions
# from tornado.wsgi import WSGIContainer
# from tornado.ioloop import IOLoop
# import tornado.web
# import tornado.httpserver
# from sockjs.tornado import SockJSRouter, SockJSConnection
from functools import wraps, partial

from opsoro.expression import Expression
from opsoro.robot import Robot
from opsoro.console_msg import *
from opsoro.preferences import Preferences
from opsoro.server.request_handlers.opsoro_data_requests import *
# from opsoro.server import AdminUser

import pluginbase
import random
import os
import subprocess
import atexit
import threading
import base64
import time
import logging

import glob
import shutil

try:
    import simplejson as json
    print_info("Using simplejson")
except ImportError:
    import json
    print_info("Simplejson not available, falling back on json")

dof_positions = {}
# Helper function
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


# Helper class to deal with login
class AdminUser(object):
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "admin"

    def is_admin(self):
        return True


class RHandler(object):
    def __init__(self, server):
        # title
        self.title = "OPSORO play"
        self.robotName = "Ono"

        self.server = server

    def set_urls(self):

        protect = self.server.protected_view

        self.server.flaskapp.add_url_rule("/",
                                          "index",
                                          protect(self.page_index), )
        self.server.flaskapp.add_url_rule(
            "/login",
            "login",
            self.page_login,
            methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/logout",
                                          "logout",
                                          self.page_logout, )
        # self.server.flaskapp.add_url_rule(
        #     "/preferences",
        #     "preferences",
        #     protect(self.page_preferences),
        #     methods=["GET", "POST"], )
        self.server.flaskapp.add_url_rule("/sockjstoken",
                                          "sockjstoken",
                                          self.page_sockjstoken, )
        self.server.flaskapp.add_url_rule("/shutdown",
                                          "shutdown",
                                          protect(self.page_shutdown), )
        self.server.flaskapp.add_url_rule("/closeapp",
                                          "closeapp",
                                          protect(self.page_closeapp), )
        self.server.flaskapp.add_url_rule("/openapp/<appname>",
                                          "openapp",
                                          protect(self.page_openapp), )
        # self.server.flaskapp.add_url_rule(
        #     "/app/<appname>/files/<action>",
        #     "files",
        #     protect(self.page_files),
        #     methods=["GET", "POST"], )
        # ----------------------------------------------------------------------
        # DOCUMENTS
        # ----------------------------------------------------------------------
        self.server.flaskapp.add_url_rule(
            "/docs/data/<app_name>/",
            "file_data",
            protect(docs_file_data),
            methods=["GET"], )
        self.server.flaskapp.add_url_rule(
            "/docs/save/<app_name>/",
            "file_save",
            protect(docs_file_save),
            methods=["POST"], )
        self.server.flaskapp.add_url_rule(
            "/docs/delete/<app_name>/",
            "file_delete",
            protect(docs_file_delete),
            methods=["POST"], )
        self.server.flaskapp.add_url_rule(
            "/docs/list/",
            "file_list",
            protect(self.page_file_list),
            methods=["GET"], )

        # ----------------------------------------------------------------------
        # ROBOT
        # ----------------------------------------------------------------------
        self.server.flaskapp.add_url_rule(
            "/robot/",
            "robot",
            self.page_virtual,
            methods=["GET", "POST"], )

        for _exc in default_exceptions:
            self.server.flaskapp.errorhandler(_exc)(self.show_errormessage)

        self.server.flaskapp.context_processor(self.inject_opsoro_vars)

    def render_template(self, template, **kwargs):
        kwargs["app"] = {}

        kwargs["title"] = self.title
        # Set app variables
        if self.server.activeapp in self.server.apps:
            kwargs["app"]["active"] = True
            kwargs["app"]["name"] = self.server.apps[
                self.server.activeapp].config["full_name"].replace('_',
                                                                   ' ').title()
            kwargs["app"]["full_name"] = self.server.apps[
                self.server.activeapp].config["full_name"].lower().replace(' ',
                                                                           '_')
            kwargs["app"]["icon"] = self.server.apps[
                self.server.activeapp].config["icon"]
            kwargs["app"]["color"] = self.server.apps[
                self.server.activeapp].config["color"]
            kwargs["title"] += " - %s" % self.server.apps[
                self.server.activeapp].config["full_name"].replace('_',
                                                                   ' ').title()
            kwargs["page_icon"] = self.server.apps[
                self.server.activeapp].config["icon"]
            kwargs["page_caption"] = self.server.apps[
                self.server.activeapp].config["full_name"]
        else:
            kwargs["app"]["active"] = False

        if 'actions' not in kwargs:
            kwargs['actions'] = {}
        kwargs['actions']['openfile'] = request.args.get("f", None)

        if "closebutton" not in kwargs:
            kwargs["closebutton"] = True

        return render_template(template, **kwargs)

    def page_index(self):
        data = {"title": self.title, "apps": []}

        if self.server.activeapp in self.server.apps:
            app = self.server.apps[self.server.activeapp]
            data["activeapp"] = {"name": self.server.activeapp,
                                 "full_name": app.config["full_name"],
                                 "icon": app.config["icon"],
                                 "color": app.config['color']}

        for appname in sorted(self.server.apps.keys()):
            app = self.server.apps[appname]
            data["apps"].append({"name": appname,
                                 "full_name": app.config["full_name"],
                                 "icon": app.config["icon"],
                                 "color": app.config['color'],
                                 "active": (appname == self.server.activeapp)})

        return self.render_template("apps.html", **data)

    def page_login(self):
        if request.method == "GET":
            return render_template("login.html", title=self.title + " - Login")

        password = request.form["password"]

        if password == Preferences.get(
                "general", "password", default="RobotOpsoro"):
            login_user(AdminUser())
            self.server.active_session_key = os.urandom(24)
            session["active_session_key"] = self.server.active_session_key
            return redirect(url_for("index"))
        else:
            flash("Wrong password.")
            return redirect(url_for("login"))

    def page_logout(self):
        logout_user()
        session.pop("active_session_key", None)
        flash("You have been logged out.")
        return redirect(url_for("login"))

    def page_sockjstoken(self):
        if current_user.is_authenticated:
            if current_user.is_admin():
                if session[
                        "active_session_key"] == self.server.active_session_key:
                    # Valid user, generate a token
                    self.server.sockjs_token = os.urandom(24)
                    return base64.b64encode(self.server.sockjs_token)
                else:
                    logout_user()
                    session.pop("active_session_key", None)
        return ""  # Not a valid user, return nothing!

    def page_shutdown(self):
        message = ""
        self.server.stop_current_app()

        # Run shutdown command with 5 second delay, returns immediately
        subprocess.Popen("sleep 5 && sudo halt", shell=True)
        self.server.shutdown_server()
        return message

    def page_closeapp(self):
        self.server.stop_current_app()
        return redirect(url_for("index"))

    def page_openapp(self, appname):
        # Check if another app is running, if so, run its stop function
        self.server.stop_current_app()

        if appname in self.server.apps:
            Robot.start()
            self.server.activeapp = appname

            try:
                print_appstarted(appname)
                self.server.apps[appname].start(self.server)
            except AttributeError:
                print_info("%s has no start function" % self.server.activeapp)

            return redirect("/apps/%s/" % appname)
        else:
            return redirect(url_for("index"))

    def page_file_list(self):
        data = docs_file_list()
        return self.render_template(
            "filelist.html",
            title=self.title + " - Files",
            # page_caption=appSpecificFolderPath,
            page_icon="fa-folder",
            **data)

    def page_virtual(self):
        clientconn = None

        # def send_stopped():
        #     global clientconn
        #     if clientconn:
        #         clientconn.send_data("soundStopped", {})

        if request.method == "POST":
            dataOnly = request.form.get("getdata", type=int, default=0)
            if dataOnly == 1:
                tempDofs = Robot.dof_values()
                return json.dumps({'success': True, 'dofs': tempDofs})
        # 		return Expression.dof_values
            frameOnly = request.form.get("frame", type=int, default=0)
            if frameOnly == 1:
                #return self.render_template("virtual.html", title="Virtual Model", page_caption="Virtual model", page_icon="fa-smile-o", modules=Modules.modules)
                pass

        file_location = get_path('../config/')
        file_name = 'default.conf'
        config_data = ''
        if os.path.isfile(file_location + file_name):
            with open(get_path(file_location + file_name), "r") as f:
                config_data = f.read()
            # config_data = send_from_directory(file_location, file_name)
            print_info("Default config loaded")

        return self.render_template(
            "virtual.html",
            title="Virtual Model",
            page_caption="Virtual model",
            page_icon="fa-smile-o",
            modules=Robot.modules,
            config=config_data)

    def show_errormessage(self, error):
        print_error(error)
        return redirect("/")
        return ""

    def page_login(self):
        if request.method == "GET":
            return render_template("login.html", title=self.title + " - Login")

        password = request.form["password"]

        if password == Preferences.get(
                "general", "password", default="RobotOpsoro"):
            login_user(AdminUser())
            self.server.active_session_key = os.urandom(24)
            session["active_session_key"] = self.server.active_session_key
            return redirect(url_for("index"))
        else:
            flash("Wrong password.")
            return redirect(url_for("login"))

    def inject_opsoro_vars(self):
        opsoro = {"robot_name": Preferences.get("general", "robot_name",
                                                self.robotName)}
        return dict(opsoro=opsoro)
