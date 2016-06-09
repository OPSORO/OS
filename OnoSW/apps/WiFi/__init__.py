from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename
from sound import Sound
# from azure.servicebus import ServiceBusService , Message , Queue
import math
import cmath

from console_msg import *
from hardware import Hardware
from stoppable_thread import StoppableThread

from functools import partial
from exceptions import RuntimeError
import os
import glob
import shutil
import time
import yaml
import subprocess
from subprocess import call
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader

from flask import Blueprint, render_template, request, send_from_directory

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

from expression import Expression

config = {"full_name": "Wi-Fi", "icon": "fa-wifi"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


# def AppLoop():
# 	while not app_t.stopped():
# 		with Expression.lock:
# 			Expression.update()
#
# 		app_t.sleep(0.015)
#
# app_t = None

def setup_pages(opsoroapp):
	app_bp = Blueprint("wifi", __name__, template_folder="templates", static_folder="static")

	@app_bp.route("/", methods=["GET"])
	@opsoroapp.app_view
	def index():
		data = {
			"actions":			{},
			"data":				[],
		}

		action = request.args.get("action", None)
		if action != None:
			data["actions"][action] = request.args.get("param", None)
			
		return opsoroapp.render_template("wifi.html", **data)


	# @app_bp.route("/demo")
	# @opsoroapp.app_view
	# def demo():
	# 	data = {
	# 	}
	#
	# 	return opsoroapp.render_template("app.html", **data)

	# @app_bp.route("/demo")
	# @opsoroapp.app_view
	# def demo():
	# 	data = {
	# 	}
	#
	# 	return opsoroapp.render_template("app.html", **data)

		

	@app_bp.route("/refresh", methods=["POST"])
	@opsoroapp.app_api
	def refresh():
		subprocess.call("sudo sh /home/pi/OnoSW/scan_wifi.sh", shell=True)


	@app_bp.route("/connect", methods=["POST"])
	@opsoroapp.app_api
	def connect():
		essid = request.form.get("essid")
		psk = request.form.get("psk")

		subprocess.call("sudo wpa_passphrase " + essid + " " + psk + " > /home/pi/WiFi/wpa.conf", shell=True)
		time.sleep(1)
		subprocess.call("sudo ifdown wlan0", shell=True)
		time.sleep(1)
		subprocess.call("sudo ifup wlan0", shell=True)


	@app_bp.route("/checkwifi", methods=["POST"])
	@opsoroapp.app_api
	def checkwifi():
		output = subprocess.check_output("sudo /sbin/ifconfig wlan0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'",shell=True)
				

		
	opsoroapp.register_app_blueprint(app_bp)

def setup(opsoroapp):
	pass

def start(opsoroapp):
	# Start update thread
	# global app_t

	# app_t = StoppableThread(target=AppLoop)
	#app_t.start();
		
	pass

def stop(opsoroapp):
	# Stop update thread
	# global app_t
	# if app_t is not None:
	# 	app_t.stop()
	pass
