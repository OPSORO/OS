from __future__ import with_statement

from functools import partial
from exceptions import RuntimeError
import os
import time

from flask import Blueprint, render_template, request

from expression_manager import ExpressionManager

config = {"full_name": "Config Editor", "icon": "fa-pencil"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

def setup_pages(onoapp):
	configeditor_bp = Blueprint("configeditor", __name__, template_folder="templates")

	@configeditor_bp.route("/")
	@onoapp.app_view
	def index():
		data = {
			"page_icon":		config["icon"],
			"page_caption":		config["full_name"],
			"title":			"Ono web interface - %s" % config["full_name"]
		}
		with open(get_path("../../config/pinmap.yaml")) as f:
			data["file_pinmap"] = f.read()
		with open(get_path("../../config/limits.yaml")) as f:
			data["file_limits"] = f.read()
		with open(get_path("../../config/functions.yaml")) as f:
			data["file_functions"] = f.read()
		return onoapp.render_template("configeditor.html", **data)

	@configeditor_bp.route("/getdefault/<filename>")
	@onoapp.app_api
	def getdefault(filename):
		if filename in ["pinmap", "limits", "functions"]:
			file = ""
			with open(get_path("../../config/%s.default.yaml" % filename)) as f:
				file = f.read()
			return {"file": file}
		else:
			return {"error": "Unknown file."}

	@configeditor_bp.route("/saveconfig/<filename>", methods=["POST"])
	@onoapp.app_api
	def saveconfig(filename):
		file = request.form.get("file", type=str, default="")

		if filename in ["pinmap", "limits", "functions"]:
			# Save a backup for logging and for parsing
			backup_filename = "%s__%s.yaml" % (filename, time.strftime("%Y-%m-%d_%H-%M-%S"))
			backup_full_path = get_path("../../../OnoSW_backups/%s" % backup_filename)
			with open(backup_full_path, "w") as f:
				f.write(file)

			try:
				kwargs = {}
				kwargs[filename] = ("../../OnoSW_backups/%s" % backup_filename)

				# Make an ExpressionManager instance to evaluate new config file
				em = ExpressionManager(onoapp.hw, **kwargs)

				# No exception, so save the new config file
				with open(get_path("../../config/%s.yaml" % filename), "w") as f:
					f.write(file)
			except Exception, e:
				return {"status": "error", "message": "Error saving config/%s.yaml:<br/> %s" % (filename, str(e))}
			return {"message": "Successfully saved config/%s.yaml" % filename}
		else:
			return {"status": "error", "message": "Unknown file."}

	onoapp.register_app_blueprint(configeditor_bp)

def setup(onoapp):
	pass

def start(onoapp):
	print "\033[95m" + "Started %s" % config["full_name"] + "\033[0m"

def stop(onoapp):
	print "\033[95m" + "Stopped %s" % config["full_name"] + "\033[0m"
