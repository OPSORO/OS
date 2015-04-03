from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

from functools import wraps, partial

from onoadminuser import OnoAdminUser
from hardware import Hardware

import yaml
import pluginbase
import random
import os
import subprocess
import atexit
import threading

# Helper function
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

class OnoApplication(object):
	def __init__(self):
		# Initialize hardware
		self.hw = Hardware()

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

		# Setup app system
		self.plugin_base = pluginbase.PluginBase(package="onoapplication.apps")
		self.plugin_source = self.plugin_base.make_plugin_source(searchpath=[get_path("./apps")])

		self.apps = {}
		self.activeapp = None
		self.apps_can_register_bp = True # Make sure apps are only registered during setup
		self.current_bp_app = "" # Keep track of current app for blueprint setup

		for plugin_name in self.plugin_source.list_plugins():
			self.current_bp_app = plugin_name

			plugin = self.plugin_source.load_plugin(plugin_name)
			print "Loaded app: ", plugin_name

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
				print "%s has no setup function" % plugin_name

			try:
				plugin.setup_pages(self)
			except AttributeError:
				print "%s has no setup_pages function" % plugin_name

		self.current_bp_app = ""
		self.apps_can_register_bp = False

		# Initialize all URLs
		self.setup_urls()

		# Run stop function at exit
		atexit.register(self.at_exit)

	def at_exit(self):
		# Check if another app is running, if so, run its stop function
		print "at_exit active app:", self.activeapp
		if threading.activeCount() > 0:
			print "Active threads:", threading.activeCount()
			threads = threading.enumerate()
			for thread in threads:
				try:
					thread.stop()
					thread.join()
				except AttributeError:
					pass
		if self.activeapp in self.apps:
			try:
				self.apps[self.activeapp].stop(self)
			except AttributeError:
				print "%s has no stop function" % self.activeapp

	def setup_user_loader(self):
		@self.login_manager.user_loader
		def load_user(id):
			if id == "admin":
				return OnoAdminUser()
			else:
				return None

	def register_app_blueprint(self, bp):
		assert self.apps_can_register_bp, "Apps can only register blueprints at setup!"

		prefix = "/app/" + self.current_bp_app
		self.flaskapp.register_blueprint(bp, url_prefix=prefix)

	def render_template(self, template, **kwargs):
		kwargs["toolbar"] = {}

		# Set toolbar variables
		if self.activeapp in self.apps:
			kwargs["toolbar"]["active"] = True
			kwargs["toolbar"]["full_name"] = self.apps[self.activeapp].config["full_name"]
			kwargs["toolbar"]["icon"] = self.apps[self.activeapp].config["icon"]
		else:
			kwargs["toolbar"]["active"] = False

		if "closebutton" not in kwargs:
			kwargs["closebutton"] = True

		return render_template(template, **kwargs)

	def run(self):
		self.flaskapp.run(host="0.0.0.0", port=80, threaded=True)

	def shutdown_server(self):
		func = request.environ.get("werkzeug.server.shutdown")
		if func is None:
			raise RuntimeError("Not running with the Werkzeug Server")
		func()

	def protected_view(self, f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			if current_user.is_authenticated():
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
			if current_user.is_authenticated():
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

				if self.activeapp in self.apps:
					# Another app is active
					data["toolbar"]["active"] = True
					data["toolbar"]["full_name"] = self.apps[self.activeapp].config["full_name"]
					data["toolbar"]["icon"] = self.apps[self.activeapp].config["icon"]
					data["title"] = "Ono Web Interface - %s" % self.apps[self.activeapp].config["full_name"]
				else:
					# No app is active
					data["toolbar"]["active"] = False
					data["title"] = "Ono Web Interface"

				return render_template("appnotactive.html", **data)
		return wrapper

	def app_api(self, f):
		appname = f.__module__.split(".")[-1]

		@wraps(f)
		def wrapper(*args, **kwargs):
			# Protected page
			if current_user.is_authenticated():
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

	def setup_urls(self):
		protect = self.protected_view
		self.flaskapp.add_url_rule("/",					"index",	protect(self.page_index))
		self.flaskapp.add_url_rule("/login",			"login",	self.page_login, methods=["GET", "POST"])
		self.flaskapp.add_url_rule("/logout",			"logout",	self.page_logout)
		self.flaskapp.add_url_rule("/shutdown",			"shutdown",	protect(self.page_shutdown))
		self.flaskapp.add_url_rule("/closeapp",			"closeapp",	protect(self.page_closeapp))
		self.flaskapp.add_url_rule("/openapp/<appname>","openapp",	protect(self.page_openapp))

	#def page_random(self):
	#	return "Hello World! %d" % random.randrange(0, 100, 1)

	def page_index(self):
		data = {
			"title":		"Ono Web Interface",
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
			return render_template("login.html", title="Ono Web Interface - Login")

		password = request.form["password"]
		# TODO: Bad practice, fix it
		if password == "RobotOno":
			login_user(OnoAdminUser())
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

	def page_shutdown(self):
		message = """
		<p>
		Shutting down...<br/> Please wait 60 seconds before cutting power.<br/>
		<span class="note">
			<strong>Note:</strong> Never power off Ono without completely shutting down first! Cutting power without properly shutting down the operating system can result in a corrupt file system.
		</span>
		"""
		# Check if another app is running, if so, run its stop function
		if self.activeapp in self.apps:
			try:
				self.apps[self.activeapp].stop(self)
			except AttributeError:
				print "%s has no stop function" % self.activeapp

		# Run shutdown command with 5 second delay, returns immediately
		subprocess.Popen("sleep 5 && sudo halt", shell=True)
		self.shutdown_server()
		return message

	def page_closeapp(self):
		if self.activeapp in self.apps:
			try:
				self.apps[self.activeapp].stop(self)
			except AttributeError:
				print "%s has no stop function" % self.activeapp

		self.activeapp = None
		return redirect(url_for("index"))

	def page_openapp(self, appname):
		# Check if another app is running, if so, run its stop function
		if self.activeapp in self.apps:
			try:
				self.apps[self.activeapp].stop(self)
			except AttributeError:
				print "%s has no stop function" % self.activeapp


		if appname in self.apps:
			self.activeapp = appname

			try:
				self.apps[appname].start(self)
			except AttributeError:
				print "%s has no start function" % appname

			return redirect("/app/%s/" % appname)
		else:
			return redirect(url_for("index"))
