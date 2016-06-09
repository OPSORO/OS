from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename
from sound import Sound

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
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader

from flask import Blueprint, render_template, request, send_from_directory

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

from expression import Expression

config = {"full_name": "Rekenwereld", "icon": "fa-calculator"}

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
	app_bp = Blueprint("rekenwereld", __name__, template_folder="templates", static_folder="static")

	@app_bp.route("/", methods=["GET"])
	@opsoroapp.app_view
	def index():
		data = {
			"actions":			{},
			"data":				[],
			"sounds":			[]
		}

		action = request.args.get("action", None)
		if action != None:
			data["actions"][action] = request.args.get("param", None)
			
		filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.wav"))

		for filename in filenames:
			data["sounds"].append(os.path.split(filename)[1])
		data["sounds"].sort()
			
		return opsoroapp.render_template("rekenwereld.html", **data)


	# @app_bp.route("/demo")
	# @opsoroapp.app_view
	# def demo():
	# 	data = {
	# 	}
	#
	# 	return opsoroapp.render_template("app.html", **data)

	@app_bp.route("/servos/enable")
	@opsoroapp.app_api
	def servosenable():
		print_info("Servos enabled")
		with Hardware.lock:
			Hardware.servo_enable()

	@app_bp.route("/servos/disable")
	@opsoroapp.app_api
	def servosdisable():
		print_info("Servos disabled")
		with Hardware.lock:
			Hardware.servo_disable()

	@app_bp.route("/setemotion", methods=["POST"])
	@opsoroapp.app_api
	def setemotion():
		phi = request.form.get("phi", type=float, default=0.0)
		r = request.form.get("r", type=float, default=0.0)

		phi = constrain(phi, 0.0, 360.0)
		r = constrain(r, 0.0, 1.0)

		phi = phi * math.pi/180.0

		# Calculate distance between old and new emotions.
		# Shorter emotional distances are animated faster than longer distances.
		#e_old = Expression.get_emotion_complex()
		#e_new = cmath.rect(r, phi)
		#dist = abs(e_new - e_old)/2

		with Expression.lock:
			Expression.set_emotion(phi=phi, r=r)#, anim_time=dist)
			# Expression is updated in separate thread, no need to do this here.
			# Expression.update()

	@app_bp.route("/play/<soundfile>", methods=["GET"])
	@opsoroapp.app_api
	def play(soundfile):
		soundfiles = []
		filenames = []

		filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.wav"))

		for filename in filenames:
			soundfiles.append(os.path.split(filename)[1])

		if soundfile in soundfiles:
			Sound.play_file(soundfile)
			return {"status": "success"}
		else:
			return {"status": "error", "message": "Unknown file."}

	@app_bp.route("/saytts", methods=["GET"])
	@opsoroapp.app_api
	def saytts():
		text = request.args.get("text", None)
		if text is not None:
			Sound.say_tts(text)
		return {"status": "success"}

	opsoroapp.register_app_blueprint(app_bp)

def setup(opsoroapp):
	pass

def start(opsoroapp):
	# Start update thread
	for servo in Expression.servos:
		if servo.pin < 0 or servo.pin > 15:
			continue # Skip invalid pins
		#dof_positions[servo.dofname] = 0.0

	# Turn servo power off, init servos, update expression
	with Hardware.lock:
		Hardware.servo_disable()
		Hardware.servo_init()
		Hardware.servo_neutral()

	with Expression.lock:
		Expression.set_emotion(valence=0.0, arousal=0.0)
		Expression.update()

	# Start update thread
	

def stop(opsoroapp):
	with Hardware.lock:
		Hardware.servo_disable()


