from functools import partial
import os
import glob
import threading
import time
from flask import Blueprint, render_template, request, send_from_directory
from werkzeug import secure_filename
import pygame
from stoppable_thread import StoppableThread
from expression_manager import ExpressionManager

config = {"full_name": "Visual Programming", "icon": "fa-puzzle-piece"}

em = None
em_lock = threading.Lock()

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

def setup_pages(onoapp):
	vp_bp = Blueprint("visualprogramming", __name__, template_folder="templates", static_folder="static")

	global em
	global em_lock

	@vp_bp.route("/")
	@onoapp.app_view
	def index():
		data = {
			"page_icon":		config["icon"],
			"page_caption":		config["full_name"],
			"title":			"Ono web interface - %s" % config["full_name"]
		}

		return onoapp.render_template("blockly.html", **data)

	@vp_bp.route("/blockly_inner")
	@onoapp.app_view
	def blockly_inner():
		data = {
			"soundfiles":		[],
			"dofnames":			[]
		}

		filenames = []

		filenames.extend(glob.glob(get_path("../sounds/soundfiles/*.wav")))
		filenames.extend(glob.glob(get_path("../sounds/soundfiles/*.mp3")))
		filenames.extend(glob.glob(get_path("../sounds/soundfiles/*.ogg")))

		for filename in filenames:
			data["soundfiles"].append(os.path.split(filename)[1])

		with em_lock:
			for dofname in em.pinmap:
				if dofname is not None:
					data["dofnames"].append(dofname)

		return onoapp.render_template("blockly_inner.html", **data)

	@vp_bp.route("/filelist")
	@onoapp.app_view
	def filelist():
		data = {
			"savefiles":	[]
		}

		filenames = []
		filenames.extend(glob.glob(get_path("saves/*.xml")))

		for filename in filenames:
			data["savefiles"].append(os.path.split(filename)[1])

		return onoapp.render_template("filelist.html", **data)

	@vp_bp.route("/save", methods=["POST"])
	@onoapp.app_api
	def save():
		file = request.form.get("file", type=str, default="")
		filename = request.form.get("filename", type=str, default="")
		overwrite = request.form.get("overwrite", type=int, default=0)

		if filename == "":
			return {"status": "error", "message": "No filename given."}

		if filename[-4:] != ".xml":
			filename = filename + ".xml"
		filename = secure_filename(filename)

		full_path = os.path.join(get_path("saves/"), filename)

		if overwrite == 0:
			if os.path.isfile(full_path):
				return {"status": "error", "message": "File already exists."}

		with open(full_path, "w") as f:
			f.write(file)

		return {"status": "success", "filename": filename}

	@vp_bp.route("/delete/<savefile>", methods=["POST"])
	@onoapp.app_api
	def delete(savefile):
		savefiles = []
		filenames = []
		filenames.extend(glob.glob(get_path("saves/*.xml")))

		for filename in filenames:
			savefiles.append(os.path.split(filename)[1])

		if savefile in savefiles:
			os.remove(os.path.join(get_path("saves/"), savefile))
			return {"status": "success", "message": "File %s deleted." % savefile}
		else:
			return {"status": "error", "message": "Unknown file."}

	@vp_bp.route("/saves/<savefile>")
	@onoapp.app_view
	def saves(savefile):
		return send_from_directory(get_path("saves/"), savefile)

	# This function is used for temp saves
	@vp_bp.route("/savecode", methods=["POST"])
	@onoapp.app_api
	def savecode():
		file = request.form.get("file", type=str, default="")

		backup_filename = "Blockly_Run__%s.xml" % time.strftime("%Y-%m-%d_%H-%M-%S")
		backup_full_path = get_path("../../../OnoSW_backups/%s" % backup_filename)

		print "Saved XML as /OnoSW_backups/%s" % backup_filename

		with open(backup_full_path, "w") as f:
			f.write(file)

		return {"status": "success"}

	@vp_bp.route("/api/playsound/<soundfile>", methods=["GET"])
	@onoapp.app_api
	def api_playsound(soundfile):
		soundfiles = []
		filenames = []

		filenames.extend(glob.glob(get_path("../sounds/soundfiles/*.wav")))
		filenames.extend(glob.glob(get_path("../sounds/soundfiles/*.mp3")))
		filenames.extend(glob.glob(get_path("../sounds/soundfiles/*.ogg")))

		for filename in filenames:
			soundfiles.append(os.path.split(filename)[1])

		if soundfile in soundfiles:
			pygame.mixer.music.load(os.path.join(get_path("../sounds/soundfiles/"), soundfile))
			pygame.mixer.music.play()
			return {"status": "success"}
		else:
			return {"status": "error", "message": "Unknown sound file."}
		return {"status": "success"}

	@vp_bp.route("/api/saytts", methods=["GET"])
	@onoapp.app_api
	def api_saytts():
		text = request.args.get("text", None)
		if text is not None:
			onoapp.hw.say_tts(text)
		return {"status": "success"}

	@vp_bp.route("/api/servoson")
	@onoapp.app_api
	def api_servoson():
		onoapp.hw.servo_power_on()
		return {"status": "success"}

	@vp_bp.route("/api/servosoff")
	@onoapp.app_api
	def api_servosoff():
		onoapp.hw.servo_power_off()
		return {"status": "success"}

	@vp_bp.route("/api/updateservos")
	@onoapp.app_api
	def api_updateservos():
		with em_lock:
			em.update_servos()
		return {"status": "success"}

	@vp_bp.route("/api/setposition", methods=["GET"])
	@onoapp.app_api
	def api_setposition():
		dofs = request.args.get("dofs", default=None)
		if dofs == "":
			dofs = None
		if dofs is not None:
			if "," in dofs:
				dofs = dofs.split(",")

		pos = request.args.get("pos", type=int, default=0)
		pos = constrain(pos, -100, 100)

		with em_lock:
			em.set_target_pos(pos, steps=0, which=dofs)

		return {"status": "success"}

	@vp_bp.route("/api/setemotion", methods=["GET"])
	@onoapp.app_api
	def api_setemotion():
		dofs = request.args.get("dofs", default=None)
		if dofs == "":
			dofs = None
		if dofs is not None:
			if "," in dofs:
				dofs = dofs.split(",")

		valence = request.args.get("valence", type=float, default=None)
		arousal = request.args.get("valence", type=float, default=None)

		alpha = request.args.get("alpha", type=float, default=None)
		length = request.args.get("length", type=float, default=None)

		if alpha is not None and length is not None:
			with em_lock:
				em.set_target_alpha_length(alpha, length, steps=0, which=dofs)
		elif valence is not None and arousal is not None:
			with em_lock:
				em.set_target_valence_arousal(valence, arousal, steps=0, which=dofs)
		else:
			return {"status": "error", "message": "Not enough parameters for setemotion."}

		return {"status": "success"}

	onoapp.register_app_blueprint(vp_bp)

def setup(onoapp):
	global em
	global em_lock
	with em_lock:
		em = ExpressionManager(onoapp.hw)
		em.all_servos_mid()

def start(onoapp):
	pygame.mixer.init()
	with em_lock:
		em.all_servos_mid()

def stop(onoapp):
	pygame.mixer.stop()
	pygame.mixer.quit()
	onoapp.hw.servo_power_off()
