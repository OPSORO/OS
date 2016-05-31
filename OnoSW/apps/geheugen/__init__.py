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

config = {"full_name": "Geheugenkoning", "icon": "fa-gamepad"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

dof_positions = {}

def SocialscriptLoop():
	while not socialscript_t.stopped():
		with Expression.lock:
			Expression.update()

		socialscript_t.sleep(0.015)

socialscript_t = None

def setup_pages(opsoroapp):
	socialscript_bp = Blueprint("geheugen", __name__, template_folder="templates", static_folder="static")

	@socialscript_bp.route("/", methods=["GET"])
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

		filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.wav"))

		for filename in filenames:
			data["sounds"].append(os.path.split(filename)[1])
		data["sounds"].sort()

		return opsoroapp.render_template("geheugen.html", **data)

	# @socialscript_bp.route("/filelist")
	# @opsoroapp.app_view
	# def filelist():
	# 	data = {
	# 		"scriptfiles":	[]
	# 	}
	#
	# 	filenames = []
	# 	filenames.extend(glob.glob(get_path("../../data/socialscript/scripts/*.soc")))
	#
	# 	for filename in filenames:
	# 		data["scriptfiles"].append(os.path.split(filename)[1])
	#
	# 	return opsoroapp.render_template("filelist.html", **data)
	#
	# @socialscript_bp.route("/save", methods=["POST"])
	# @opsoroapp.app_api
	# def save():
	# 	socfile = request.form.get("file", type=str, default="")
	# 	filename = request.form.get("filename", type=str, default="")
	# 	overwrite = request.form.get("overwrite", type=int, default=0)
	#
	# 	if filename == "":
	# 		return {"status": "error", "message": "No filename given."}
	#
	# 	if filename[-4:] != ".soc":
	# 		filename = filename + ".soc"
	# 	filename = secure_filename(filename)
	#
	# 	full_path = os.path.join(get_path("../../data/socialscript/scripts/"), filename)
	#
	# 	if overwrite == 0:
	# 		if os.path.isfile(full_path):
	# 			return {"status": "error", "message": "File already exists."}
	#
	# 	with open(full_path, "w") as f:
	# 		f.write(socfile)
	#
	# 	return {"status": "success", "filename": filename}
	#
	# @socialscript_bp.route("/delete/<scriptfile>", methods=["POST"])
	# @opsoroapp.app_api
	# def delete(scriptfile):
	# 	scriptfiles = []
	# 	filenames = []
	# 	filenames.extend(glob.glob(get_path("../../data/socialscript/scripts/*.soc")))
	#
	# 	for filename in filenames:
	# 		scriptfiles.append(os.path.split(filename)[1])
	#
	# 	if scriptfile in scriptfiles:
	# 		os.remove(os.path.join(get_path("../../data/socialscript/scripts/"), scriptfile))
	# 		return {"status": "success", "message": "File %s deleted." % scriptfile}
	# 	else:
	# 		return {"status": "error", "message": "Unknown file."}
	#
	# @socialscript_bp.route("/scripts/<scriptfile>")
	# @opsoroapp.app_view
	# def scripts(scriptfile):
	# 	return send_from_directory(get_path("../../data/socialscript/scripts/"), scriptfile)
	#
	#
	# @socialscript_bp.route("/file", methods=["GET"])
	# @opsoroapp.app_view
	# def file():
	# 	scriptfile = request.args.get("script", None)
	# 	#scriptfile = request.form.get("script", type=str, default="")
	# 	return send_from_directory(get_path("../../"), scriptfile)

	@socialscript_bp.route("/servos/enable")
	@opsoroapp.app_api
	def servosenable():
		print_info("Servos enabled")
		with Hardware.lock:
			Hardware.servo_enable()

	@socialscript_bp.route("/servos/disable")
	@opsoroapp.app_api
	def servosdisable():
		print_info("Servos disabled")
		with Hardware.lock:
			Hardware.servo_disable()

	@socialscript_bp.route("/setemotion", methods=["POST"])
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


	@socialscript_bp.route("/play/<soundfile>", methods=["GET"])
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

	@socialscript_bp.route("/saytts", methods=["GET"])
	@opsoroapp.app_api
	def saytts():
		text = request.args.get("text", None)
		if text is not None:
			Sound.say_tts(text)
		return {"status": "success"}

	@socialscript_bp.route("/setDofPos", methods=["POST"])
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

	opsoroapp.register_app_blueprint(socialscript_bp)

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
