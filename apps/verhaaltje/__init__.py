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

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

from expression import Expression

config = {"full_name": "Verhaaltjestijd", "icon": "fa-book"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

dof_positions = {}

def SocialscriptLoop():
	while not socialscript_t.stopped():
		with Expression.lock:
			Expression.update()

		socialscript_t.sleep(0.015)

socialscript_t = None

def setup_pages(opsoroapp):
	app_bp = Blueprint("verhaaltje", __name__, template_folder="templates", static_folder="static")

	@app_bp.route("/", methods=["GET"])
	@opsoroapp.app_view
	def index():
		data = {
			"actions":			{},
			"emotions":			[],
			"sounds":			[]
		}

		action = request.args.get("action", None)
		if action != None:
			data["actions"][action] = request.args.get("param", None)

		with open(get_path("emotions.yaml")) as f:
			data["emotions"] = yaml.load(f, Loader=Loader)

		filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.txt"))

		for filename in filenames:
			data["sounds"].append(os.path.split(filename)[1])
		data["sounds"].sort()

		return opsoroapp.render_template("verhaaltje.html", **data)

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

		filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.txt"))

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

	@app_bp.route("/setDofPos", methods=["POST"])
	@opsoroapp.app_api
	def s_setdofpos():
		dofname = left_brow_inner = request.form.get("dofname", type=str, default=None)
		pos = request.form.get("pos", type=float, default=0.0)

		if dofname is None:
			return {"status": "error", "message": "No DOF name given."}

		global dof_positions
		if dofname not in dof_positions:
			return {"status": "error", "message": "Unknown DOF name."}
		else:
			pos = constrain(pos, -1.0, 1.0)
			dof_positions[dofname] = pos

			# with Expression.lock:
			# 	Expression.update()

		return {"status": "success"}

	opsoroapp.register_app_blueprint(app_bp)

def setup(opsoroapp):
	pass

def start(opsoroapp):
	# Apply overlay function
	for servo in Expression.servos:
		if servo.pin < 0 or servo.pin > 15:
			continue # Skip invalid pins
		dof_positions[servo.dofname] = 0.0

	# Turn servo power off, init servos, update expression
	with Hardware.lock:
		Hardware.servo_disable()
		Hardware.servo_init()
		Hardware.servo_neutral()

	with Expression.lock:
		Expression.set_emotion(valence=0.0, arousal=0.0)
		Expression.update()

	# Start update thread
	global socialscript_t
	socialscript_t = StoppableThread(target=SocialscriptLoop)
	socialscript_t.start();

def stop(opsoroapp):
	with Hardware.lock:
		Hardware.servo_disable()

	global socialscript_t
	if socialscript_t is not None:
		socialscript_t.stop()
