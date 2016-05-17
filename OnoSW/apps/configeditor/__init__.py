from __future__ import with_statement

from functools import partial
from exceptions import RuntimeError
import os
import shutil
import time

from flask import Blueprint, render_template, request, send_from_directory

from expression import Expression

config = {"full_name": "Config Editor", "icon": "fa-pencil"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

def setup_pages(opsoroapp):
	configeditor_bp = Blueprint("configeditor", __name__, template_folder="templates", static_folder="static")

	@configeditor_bp.route("/")
	@opsoroapp.app_view
	def index():
		data = {
		}
		with open(get_path("../../config/pinmap.yaml")) as f:
			data["file_pinmap"] = f.read()
		with open(get_path("../../config/limits.yaml")) as f:
			data["file_limits"] = f.read()
		with open(get_path("../../config/functions.yaml")) as f:
			data["file_functions"] = f.read()
		return opsoroapp.render_template("configeditor.html", **data)

	@configeditor_bp.route("/default/<configfile>")
	@opsoroapp.app_view
	def default(configfile):
		if configfile in ["pinmap.yaml", "limits.yaml", "functions.yaml"]:
			filename = configfile[:-5] + ".default.yaml"
			return send_from_directory(get_path("../../config/"), filename)
		else:
			abort(404)

	@configeditor_bp.route("/saveconfig", methods=["POST"])
	@opsoroapp.app_api
	def saveconfig():
		pinmap_yaml = request.form.get("pinmap", type=str, default="")
		limits_yaml = request.form.get("limits", type=str, default="")
		functions_yaml = request.form.get("functions", type=str, default="")

		# Back up old config files.
		for filename in ["pinmap.yaml", "limits.yaml", "functions.yaml"]:
			src = get_path("../../config/%s" % filename)
			dst = get_path("../../config/%s.bak" % filename)
			shutil.copyfile(src, dst)

		# Copy contents to config files.
		with open(get_path("../../config/pinmap.yaml"), "w") as f:
			f.write(pinmap_yaml)

		with open(get_path("../../config/limits.yaml"), "w") as f:
			f.write(limits_yaml)

		with open(get_path("../../config/functions.yaml"), "w") as f:
			f.write(functions_yaml)

		# Evaluate configs
		try:
			Expression.load_config()
		except e:
			err_msg = str(e)

			# Restore config file backups.
			for filename in ["pinmap.yaml", "limits.yaml", "functions.yaml"]:
				src = get_path("../../config/%s.bak" % filename)
				dst = get_path("../../config/%s" % filename)
				shutil.copyfile(src, dst)

			Expression.load_config()
			return {"status": "error", "message": "Error parsing configuration files:<br/> %s<br><br> Previous configuration was restored." % err_msg}
		else:
			return {"message": "Successfully saved and parsed configuration files.<br>Loaded %d DOFs and %d servos." % (len(Expression.servos), len(Expression.dofs))}

	opsoroapp.register_app_blueprint(configeditor_bp)

def setup(opsoroapp):
	pass

def start(opsoroapp):
	pass

def stop(opsoroapp):
	pass
