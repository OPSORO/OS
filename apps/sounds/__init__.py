from __future__ import with_statement

from functools import partial
import os
import glob
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug import secure_filename
from sound import Sound

config = {"full_name": "Sounds", "icon": "fa-volume-up"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

def setup_pages(opsoroapp):
	sounds_bp = Blueprint("sounds", __name__, template_folder="templates", static_folder="static")

	@sounds_bp.route("/")
	@opsoroapp.app_view
	def index():
		data = {
			"soundfiles": 		[]
		}

		filenames = []

		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.wav")))
		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.mp3")))
		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.ogg")))

		for filename in filenames:
			data["soundfiles"].append(os.path.split(filename)[1])

		return opsoroapp.render_template("sounds.html", **data)

	@sounds_bp.route("/upload", methods=["POST"])
	@opsoroapp.app_view
	def upload():
		file = request.files["soundfile"]
		if file:
			if file.filename.rsplit('.', 1)[1] in ["wav", "mp3", "ogg"]:
				filename = secure_filename(file.filename)
				file.save(os.path.join(get_path("../../data/sounds/soundfiles/"), filename))
				flash("%s uploaded successfully." % file.filename, "success")
				return redirect(url_for(".index"))
			else:
				flash("This type of file is not allowed.", "error")
				return redirect(url_for(".index"))
		else:
			flash("No file selected.", "error")
			return redirect(url_for(".index"))

	@sounds_bp.route("/delete/<soundfile>", methods=["POST"])
	@opsoroapp.app_api
	def delete(soundfile):
		soundfiles = []
		filenames = []

		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.wav")))
		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.mp3")))
		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.ogg")))

		for filename in filenames:
			soundfiles.append(os.path.split(filename)[1])

		if soundfile in soundfiles:
			os.remove(os.path.join(get_path("../../data/sounds/soundfiles/"), soundfile))
			return {"status": "success", "message": "File %s deleted." % soundfile}
		else:
			return {"status": "error", "message": "Unknown file."}

	@sounds_bp.route("/play/<soundfile>", methods=["GET"])
	@opsoroapp.app_api
	def play(soundfile):
		soundfiles = []
		filenames = []

		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.wav")))
		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.mp3")))
		filenames.extend(glob.glob(get_path("../../data/sounds/soundfiles/*.ogg")))

		for filename in filenames:
			soundfiles.append(os.path.split(filename)[1])

		if soundfile in soundfiles:
			Sound.play_file(soundfile)
			return {"status": "success"}
		else:
			return {"status": "error", "message": "Unknown file."}

	@sounds_bp.route("/saytts", methods=["GET"])
	@opsoroapp.app_api
	def saytts():
		text = request.args.get("text", None)
		if text is not None:
			Sound.say_tts(text)
		return {"status": "success"}

	opsoroapp.register_app_blueprint(sounds_bp)

def setup(opsoroapp):
	pass

def start(opsoroapp):
	pass

def stop(opsoroapp):
	pass
