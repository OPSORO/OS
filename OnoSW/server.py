from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.exceptions import default_exceptions
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
import tornado.web
import tornado.httpserver
from sockjs.tornado import SockJSRouter, SockJSConnection
from functools import wraps, partial
import hardware
import expression
from expression import Expression
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

from console_msg import *
from preferences import Preferences
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

class OpSoRoApplication(object):
	def __init__(self):
		# title
		self.title = "OpSoRo Web Interface"
		self.robotName = "Ono"
		self.dataPath = "data/"

		# Create flask instance for webserver
		self.flaskapp = Flask(__name__)

		# Setup key for sessions
		self.flaskapp.secret_key = "5\x075y\xfe$\x1aV\x1c<A\xf4\xc1\xcfst0\xa49\x9e@\x0b\xb2\x17"

		# Setup login manager
		self.login_manager = LoginManager()
		self.login_manager.init_app(self.flaskapp)
		self.login_manager.login_view = "login"
		self.setup_user_loader()

		# Variable to keep track of the active user
		self.active_session_key = None

		# Token to authenticate socket connections
		# Client requests token via AJAX, server generates token if session is valid
		# Client then sends the token to the server via SockJS, validating the connection
		self.sockjs_token = None

		# Setup app system
		self.plugin_base = pluginbase.PluginBase(package="server.apps")
		self.plugin_source = self.plugin_base.make_plugin_source(searchpath=[get_path("./apps")])

		self.apps = {}
		self.activeapp = None
		self.apps_can_register_bp = True # Make sure apps are only registered during setup
		self.current_bp_app = "" # Keep track of current app for blueprint setup

		# Socket callback dicts
		self.sockjs_connect_cb = {}
		self.sockjs_disconnect_cb = {}
		self.sockjs_message_cb = {}

		for plugin_name in self.plugin_source.list_plugins():
			self.current_bp_app = plugin_name

			plugin = self.plugin_source.load_plugin(plugin_name)
			print_apploaded(plugin_name)

			if not hasattr(plugin, "config"):
				plugin.config = {"full_name": "No name", "icon": "fa-warning"}

			if "full_name" not in plugin.config:
				plugin.config["full_name"] = "No name"

			if "icon" not in plugin.config:
				plugin.config["icon"] = "fa-warning"

			self.apps[plugin_name] = plugin
			try:
				plugin.setup(self)
			except AttributeError:
				print_info("%s has no setup function" % plugin_name)

			try:
				plugin.setup_pages(self)
			except AttributeError:
				print_info("%s has no setup_pages function" % plugin_name)

		self.current_bp_app = ""
		self.apps_can_register_bp = False

		# Initialize all URLs
		self.setup_urls()

		# Run stop function at exit
		atexit.register(self.at_exit)

	def at_exit(self):
		self.stop_current_app()

		if threading.activeCount() > 0:
			threads = threading.enumerate()
			for thread in threads:
				try:
					thread.stop()
					thread.join()
				except AttributeError:
					pass

	def setup_user_loader(self):
		@self.login_manager.user_loader
		def load_user(id):
			if id == "admin":
				return AdminUser()
			else:
				return None

	def register_app_blueprint(self, bp):
		assert self.apps_can_register_bp, "Apps can only register blueprints at setup!"

		prefix = "/app/" + self.current_bp_app
		self.flaskapp.register_blueprint(bp, url_prefix=prefix)

	def render_template(self, template, **kwargs):
		kwargs["toolbar"] = {}

		kwargs["title"] = self.title
		# Set toolbar variables
		if self.activeapp in self.apps:
			kwargs["toolbar"]["active"] = True
			kwargs["toolbar"]["full_name"] = self.apps[self.activeapp].config["full_name"]
			kwargs["toolbar"]["icon"] = self.apps[self.activeapp].config["icon"]
			kwargs["title"] += " - %s" % self.apps[self.activeapp].config["full_name"]
			kwargs["page_icon"] = self.apps[self.activeapp].config["icon"]
			kwargs["page_caption"] = self.apps[self.activeapp].config["full_name"]
		else:
			kwargs["toolbar"]["active"] = False

		if "closebutton" not in kwargs:
			kwargs["closebutton"] = True

		return render_template(template, **kwargs)

	def run(self):
		# Setup SockJS
		class OpSoRoSocketConnection(SockJSConnection):
			def __init__(conn, *args, **kwargs):
				super(OpSoRoSocketConnection, conn).__init__(*args, **kwargs)
				conn._authenticated = False
				conn._activeapp = self.activeapp

			def on_message(conn, msg):
				# Attempt to decode JSON
				try:
					message = json.loads(msg)
				except ValueError:
					conn.send_error("Invalid JSON")
					return

				if not conn._authenticated:
					# Attempt to authenticate the socket
					try:
						if message["action"] == "authenticate":
							token = base64.b64decode(message["token"])
							if token == self.sockjs_token and self.sockjs_token is not None:
								# Auth succeeded
								conn._authenticated = True

								# Trigger connect callback
								if conn._activeapp in self.sockjs_connect_cb:
									self.sockjs_connect_cb[conn._activeapp](conn)

								return

						# Auth failed
						return
					except KeyError:
						# Auth failed
						return
				else:
					# Decode action and trigger callback, if it exists.
					action = message.pop("action", "")
					if conn._activeapp in self.sockjs_message_cb:
						if action in self.sockjs_message_cb[conn._activeapp]:
							self.sockjs_message_cb[conn._activeapp][action](conn, message)

			def on_open(conn, info):
				# Connect callback is triggered when socket is authenticated.
				pass

			def on_close(conn):
				if conn._authenticated:
					if conn._activeapp in self.sockjs_disconnect_cb:
						self.sockjs_disconnect_cb[conn._activeapp](conn)

			def send_error(conn, message):
				return conn.send(json.dumps({
					"action": "error",
					"status": "error",
					"message": message
				}))

			def send_data(conn, action, data):
				msg = {"action": action, "status": "success"}
				msg.update(data)
				return conn.send(json.dumps(msg))

		flaskwsgi = WSGIContainer(self.flaskapp)
		socketrouter = SockJSRouter(OpSoRoSocketConnection, "/sockjs")

		tornado_app = tornado.web.Application(socketrouter.urls + [(r".*", tornado.web.FallbackHandler, {"fallback": flaskwsgi})] )
		tornado_app.listen(80)

		# http_server = tornado.httpserver.HTTPServer(tornado_app, ssl_options={
		# 	"certfile": "/etc/ssl/certs/server.crt",
		# 	"keyfile": "/etc/ssl/private/server.key",
		# 	})
		# http_server.listen(443)
		try:
			IOLoop.instance().start()
		except KeyboardInterrupt:
			self.stop_current_app()
			print "Goodbye!"

	def stop_current_app(self):
		if self.activeapp in self.apps:
			print_appstopped(self.activeapp)
			try:
				self.apps[self.activeapp].stop(self)
			except AttributeError:
				print_info("%s has no stop function" % self.activeapp)
		self.activeapp = None

	def shutdown_server(self):
		logging.info("Stopping http server")
		io_loop = IOLoop.instance()
		io_loop.stop()

	def protected_view(self, f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			if current_user.is_authenticated:
				if current_user.is_admin():
					if session["active_session_key"] == self.active_session_key:
						# the actual page
						return f(*args, **kwargs)
					else:
						logout_user()
						session.pop("active_session_key", None)
						flash("You have been logged out because a more recent session is active.")
						return redirect(url_for("login"))
				else:
					flash("You do not have permission to access the requested page. Please log in below.")
					return redirect(url_for("login"))
			else:
				flash("You do not have permission to access the requested page. Please log in below.")
				return redirect(url_for("login"))
		return wrapper

	def app_view(self, f):
		appname = f.__module__.split(".")[-1]

		@wraps(f)
		def wrapper(*args, **kwargs):
			# Protected page
			if current_user.is_authenticated:
				if current_user.is_admin():
					if session["active_session_key"] != self.active_session_key:
						logout_user()
						session.pop("active_session_key", None)
						flash("You have been logged out because a more recent session is active.")
						return redirect(url_for("login"))
				else:
					flash("You do not have permission to access the requested page. Please log in below.")
					return redirect(url_for("login"))
			else:
				flash("You do not have permission to access the requested page. Please log in below.")
				return redirect(url_for("login"))

			# Check if app is active
			if appname == self.activeapp:
				# This app is active
				return f(*args, **kwargs)
			else:
				# Return app not active page
				assert appname in self.apps, "Could not find %s in list of loaded apps." % appname
				data = {
					"toolbar": {},
					"appname": appname,
					"page_icon": self.apps[appname].config["icon"],
					"page_caption": self.apps[appname].config["full_name"]
				}
				data["title"] = self.title
				if self.activeapp in self.apps:
					# Another app is active
					data["toolbar"]["active"] = True
					data["toolbar"]["full_name"] = self.apps[self.activeapp].config["full_name"]
					data["toolbar"]["icon"] = self.apps[self.activeapp].config["icon"]
					data["title"] += " - %s" % self.apps[self.activeapp].config["full_name"]
				else:
					# No app is active
					data["toolbar"]["active"] = False

				return render_template("app_not_active.html", **data)
		return wrapper

	def app_api(self, f):
		appname = f.__module__.split(".")[-1]

		@wraps(f)
		def wrapper(*args, **kwargs):
			# Protected page
			if current_user.is_authenticated:
				if current_user.is_admin():
					if session["active_session_key"] != self.active_session_key:
						logout_user()
						session.pop("active_session_key", None)
						return jsonify(status="error", message="You have been logged out because a more recent session is active.")
				else:
					return jsonify(status="error", message="You do not have permission to access the requested page.")
			else:
				return jsonify(status="error", message="You do not have permission to access the requested page.")

			# Check if app is active
			if appname == self.activeapp:
				# This app is active
				data = f(*args, **kwargs)
				if data is None:
					data = {}
				if "status" not in data:
					data["status"] = "success"

				return jsonify(data)
			else:
				# Return app not active page
				assert appname in self.apps, "Could not find %s in list of loaded apps." % appname

				return jsonify(status="error", message="This app is not active.")
		return wrapper

	def app_socket_connected(self, f):
		appname = f.__module__.split(".")[-1]

		self.sockjs_connect_cb[appname] = f

		return f

	def app_socket_disconnected(self, f):
		appname = f.__module__.split(".")[-1]

		self.sockjs_disconnect_cb[appname] = f

		return f

	def app_socket_message(self, action=""):
		def inner(f):
			appname = f.__module__.split(".")[-1]

			# Create new dict for app if necessary
			if appname not in self.sockjs_message_cb:
				self.sockjs_message_cb[appname] = {}

			self.sockjs_message_cb[appname][action] = f

			return f

		return inner

	def setup_urls(self):
		protect = self.protected_view

		self.flaskapp.add_url_rule("/",									"index",		protect(self.page_index))
		self.flaskapp.add_url_rule("/login",							"login",		self.page_login, methods=["GET", "POST"])
		self.flaskapp.add_url_rule("/logout",							"logout",		self.page_logout)
		self.flaskapp.add_url_rule("/preferences",						"preferences",	protect(self.page_preferences), methods=["GET", "POST"])
		self.flaskapp.add_url_rule("/sockjstoken",						"sockjstoken",	self.page_sockjstoken)
		self.flaskapp.add_url_rule("/shutdown",							"shutdown",		protect(self.page_shutdown))
		self.flaskapp.add_url_rule("/closeapp",							"closeapp",		protect(self.page_closeapp))
		self.flaskapp.add_url_rule("/openapp/<appname>",				"openapp",		protect(self.page_openapp))
		self.flaskapp.add_url_rule("/app/<appname>/files/<action>",		"files",		protect(self.page_files), methods=["GET", "POST"])

		self.flaskapp.add_url_rule("/virtual",							"virtual",		self.page_virtual, methods=["GET", "POST"])

		for _exc in default_exceptions:
			self.flaskapp.errorhandler(_exc)(self.show_errormessage)

		self.flaskapp.context_processor(self.inject_opsoro_vars)

	def page_index(self):
		data = {
			"title":		self.title,
			"apps":			[]
		}

		if self.activeapp in self.apps:
			app = self.apps[self.activeapp]
			data["activeapp"] = {"name": self.activeapp, "full_name": app.config["full_name"], "icon": app.config["icon"]}

		for appname in sorted(self.apps.keys()):
			app = self.apps[appname]
			data["apps"].append({"name": appname, "full_name": app.config["full_name"], "icon": app.config["icon"], "active": (appname == self.activeapp)})

		return self.render_template("apps.html", **data)

	def page_login(self):
		if request.method == "GET":
			return render_template("login.html", title=self.title + " - Login")

		password = request.form["password"]

		if password == Preferences.get("general", "password", default="RobotOpsoro"):
			login_user(AdminUser())
			self.active_session_key = os.urandom(24)
			session["active_session_key"] = self.active_session_key
			return redirect(url_for("index"))
		else:
			flash("Wrong password.")
			return redirect(url_for("login"))

	def page_logout(self):
		logout_user()
		session.pop("active_session_key", None)
		flash("You have been logged out.")
		return redirect(url_for("login"))

	def page_preferences(self):
		if request.method == "POST":
			# Update preferences
			Preferences.set("general", "robot_name", request.form["robotName"])

			if request.form["robotPassword"] == request.form["robotPasswordConfirm"]:
				if request.form["robotPassword"] != "":
					Preferences.set("general", "password", request.form["robotPassword"])

			Preferences.set("audio", "master_volume", request.form.get("volume", type=int))
			Preferences.set("audio", "tts_engine", request.form["ttsEngine"])
			Preferences.set("audio", "tts_language", request.form["ttsLanguage"])
			Preferences.set("audio", "tts_gender", request.form["ttsGender"])

			Preferences.set("wireless", "ssid", request.form["wirelessSsid"])
			Preferences.set("wireless", "channel", request.form.get("wirelessChannel", type=int))

			if request.form.get("wirelessSamePass", None) == "on":
				# Set to same password
				Preferences.set("wireless", "password", Preferences.get("general", "password", "RobotOpsoro"))
			else:
				if request.form["wirelessPassword"] == request.form["wirelessPasswordConfirm"]:
					if request.form["wirelessPassword"] != "":
						Preferences.set("wireless", "password", request.form["wirelessPassword"])

			flash("Preferences have been saved.", "success")
			Preferences.save_prefs()
			Preferences.apply_prefs(update_audio=True, update_wireless=True, restart_wireless=False)

		# Prepare json string with prefs data
		prefs = {
			"general": {
				"robotName": Preferences.get("general", "robot_name", self.robotName)
			},
			"audio": {
				"volume": Preferences.get("audio", "master_volume", 66),
				"ttsEngine": Preferences.get("audio", "tts_engine", "pico"),
				"ttsLanguage": Preferences.get("audio", "tts_language", "nl"),
				"ttsGender": Preferences.get("audio", "tts_gender", "m")
			},
			"wireless": {
				"ssid": Preferences.get("wireless", "ssid", self.robotName + "_AP"),
				"samePassword": Preferences.get("general", "password", "RobotOpsoro") == Preferences.get("wireless", "password", "RobotOpsoro"),
				"channel": Preferences.get("wireless", "channel", "1")
			}
		}

		return self.render_template("preferences.html", title=self.title + " - Preferences", page_caption="Preferences", page_icon="fa-cog", closebutton=False, prefs=prefs)

	def page_sockjstoken(self):
		if current_user.is_authenticated:
			if current_user.is_admin():
				if session["active_session_key"] == self.active_session_key:
					# Valid user, generate a token
					self.sockjs_token = os.urandom(24)
					return base64.b64encode(self.sockjs_token)
				else:
					logout_user()
					session.pop("active_session_key", None)
		return "" # Not a valid user, return nothing!

	def page_shutdown(self):
		message = ""
		self.stop_current_app()

		# Run shutdown command with 5 second delay, returns immediately
		subprocess.Popen("sleep 5 && sudo halt", shell=True)
		self.shutdown_server()
		return message

	def page_closeapp(self):
		self.stop_current_app()
		return redirect(url_for("index"))

	def page_openapp(self, appname):
		# Check if another app is running, if so, run its stop function
		self.stop_current_app()

		if appname in self.apps:
			self.activeapp = appname

			try:
				print_appstarted(appname)
				self.apps[appname].start(self)
			except AttributeError:
				print_info("%s has no start function" % self.activeapp)

			return redirect("/app/%s/" % appname)
		else:
			return redirect(url_for("index"))

	def page_files(self, appname, action):
		#
		if self.activeapp != appname:
			return redirect("/openapp/%s" % appname)
		deafultPath = self.dataPath + appname
		folderPath = deafultPath + "/"
		appSpecificFolderPath = ""
		extension = ".*"
		saveFileView = 0
		onlyFolders = 0

		if request.method == "POST":
			givenPath = request.form.get("path", type=str, default=None)
			if givenPath != None:
				if len(givenPath) > 1 and givenPath[-1] == ".":
					givenPath = givenPath[0:-1]
				givenPath = folderPath + givenPath

				extension = request.form.get("extension", type=str, default="")
				if givenPath[-len(extension):] != extension:
					givenPath = givenPath + extension

				print_info("Files: " + action + ": " + givenPath)

				# Make sure the file operations stay within the data folder
				if givenPath.find("..") >= 0:
					givenPath = None

			if action == "get":
				if givenPath == None:
					return json.dumps({'success':False}), 200, {'ContentType':'application/json'}
				givenPath.replace("%2F", "/")
				return send_from_directory(get_path(""), givenPath)

			if action == "delete":
				if givenPath == None:
					return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

				givenPath = get_path(givenPath)

				deleted = False

				if os.path.isdir(givenPath):
					shutil.rmtree(givenPath)
					deleted = True

				if os.path.isfile(givenPath):
					os.remove(os.path.join(get_path(""), givenPath))
					deleted = True

				if deleted:
					return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
				else:
					return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

			if action == "save":
				if givenPath == None:
					return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

				filedata = request.form.get("filedata", type=str, default="")
				overwrite = request.form.get("overwrite", type=int, default=0)

				givenPath = get_path(givenPath)

				if overwrite == 0:
					if os.path.isfile(givenPath):
						return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

				with open(givenPath, "w") as f:
					f.write(filedata)

				return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

			if action == "newfolder":
				if givenPath == None:
					return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

				givenPath = get_path(givenPath)
				if not os.path.exists(givenPath):
					os.makedirs(givenPath)
				else:
					return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

				return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

			appSpecificFolderPath = request.form.get("path", type=str, default="")
			extension = request.form.get("extension", type=str, default=extension)
			onlyFolders = request.form.get("onlyfolders", type=int, default=0)
			saveFileView = request.form.get("savefileview", type=int, default=0)

			while len(appSpecificFolderPath) > 0 and appSpecificFolderPath[0] == "/":
				appSpecificFolderPath = appSpecificFolderPath[1:]

			folderPath = folderPath + appSpecificFolderPath

			if len(appSpecificFolderPath) > 0 and appSpecificFolderPath[-1] != "/":
				appSpecificFolderPath = appSpecificFolderPath + "/"

			if folderPath[-1] != "/":
				folderPath = folderPath + "/"
			# Security check, should stay within data folder
			if folderPath.find("..") >= 0:
				folderPath = deafultPath
			if appSpecificFolderPath.find("..") >= 0:
				appSpecificFolderPath = ""

		data = {
			"path": appSpecificFolderPath,
			"folders": [],
			"files": []
		}
		# Only add a previous path if it is not in the base folder
		if appSpecificFolderPath[0:-1] != "":
			data["previouspath"] = appSpecificFolderPath[0:appSpecificFolderPath.rfind("/", 0, len(appSpecificFolderPath)-1)] + "/"
			if appSpecificFolderPath.rfind("/", 0, len(appSpecificFolderPath)-1) < 0:
				data["previouspath"] = "/"

		foldernames = glob.glob(get_path(folderPath + "*"))
		for foldername in foldernames:
			if ("." not in os.path.split(foldername)[1]):
				data["folders"].append(os.path.split(foldername)[1] + "/")
		data["folders"].sort()

		if (saveFileView == 1):
			data["savefileview"] = saveFileView

		if (onlyFolders != 1):
			filenames = glob.glob(get_path(folderPath + "*" + extension))
			for filename in filenames:
				if ("." in os.path.split(filename)[1]):
					data["files"].append(os.path.split(filename)[1])
			data["files"].sort()
		else:
			data["onlyfolders"] = onlyFolders

		return self.render_template("filelist.html", title=self.title + " - Files", page_caption=appSpecificFolderPath, page_icon="fa-folder", **data)

	def page_virtual(self):
		if request.method == "POST":
			dataOnly = request.form.get("getdata", type=int, default=0)
			if dataOnly == 1:
				return json.dumps({'success':False, 'dofs': Expression.dof_values})
		# 		return Expression.dof_values
			frameOnly = request.form.get("frame", type=int, default=0)
			if frameOnly == 1:
				#return self.render_template("virtual.html", title="Virtual Model", page_caption="Virtual model", page_icon="fa-smile-o", dofs=Expression.dof_values)
				pass
		return self.render_template("virtual.html", title="Virtual Model", page_caption="Virtual model", page_icon="fa-smile-o", dofs=Expression.dof_values)

	def show_errormessage(self, error):
		return redirect("http://play.opsoro.be/")

	def inject_opsoro_vars(self):
		opsoro = {"robot_name": Preferences.get("general", "robot_name", self.robotName)}
		return dict(opsoro=opsoro)
