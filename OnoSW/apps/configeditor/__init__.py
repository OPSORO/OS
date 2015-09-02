from __future__ import with_statement

from functools import partial
from exceptions import RuntimeError
import os
import shutil
import time

from flask import Blueprint, render_template, request, send_from_directory

# from expression_manager import ExpressionManager
from expression import Expression

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

	# @configeditor_bp.route("/getdefault/<filename>")
	# @onoapp.app_api
	# def getdefault(filename):
	# 	if filename in ["pinmap", "limits", "functions"]:
	# 		file = ""
	# 		with open(get_path("../../config/%s.default.yaml" % filename)) as f:
	# 			file = f.read()
	# 		return {"file": file}
	# 	else:
	# 		return {"error": "Unknown file."}

	@configeditor_bp.route("/default/<configfile>")
	@onoapp.app_view
	def default(configfile):
		if configfile in ["pinmap.yaml", "limits.yaml", "functions.yaml"]:
			filename = configfile[:-5] + ".default.yaml"
			return send_from_directory(get_path("../../config/"), filename)
		else:
			abort(404)

	@configeditor_bp.route("/saveconfig", methods=["POST"])
	@onoapp.app_api
	def saveconfig():
		pinmap_yaml = request.form.get("pinmap", type=str, default="")
		limits_yaml = request.form.get("limits", type=str, default="")
		functions_yaml = request.form.get("functions", type=str, default="")

		# print "Pinmap:"
		# print pinmap_yaml
		#
		# print "Limits:"
		# print limits_yaml
		#
		# print "Functions:"
		# print functions_yaml

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


	# @configeditor_bp.route("/saveconfig/<filename>", methods=["POST"])
	# @onoapp.app_api
	# def saveconfig(filename):
	# 	file = request.form.get("file", type=str, default="")
	#
	# 	if filename in ["pinmap", "limits", "functions"]:
	# 		# Save a backup for logging and for parsing
	# 		backup_filename = "%s__%s.yaml" % (filename, time.strftime("%Y-%m-%d_%H-%M-%S"))
	# 		backup_full_path = get_path("../../../OnoSW_backups/%s" % backup_filename)
	# 		with open(backup_full_path, "w") as f:
	# 			f.write(file)
	#
	# 		try:
	# 			kwargs = {}
	# 			kwargs[filename] = ("../../OnoSW_backups/%s" % backup_filename)
	#
	# 			# Make an ExpressionManager instance to evaluate new config file
	# 			em = ExpressionManager(onoapp.hw, **kwargs)
	#
	# 			# No exception, so save the new config file
	# 			with open(get_path("../../config/%s.yaml" % filename), "w") as f:
	# 				f.write(file)
	# 		except Exception, e:
	# 			return {"status": "error", "message": "Error saving config/%s.yaml:<br/> %s" % (filename, str(e))}
	# 		return {"message": "Successfully saved config/%s.yaml" % filename}
	# 	else:
	# 		return {"status": "error", "message": "Unknown file."}

	onoapp.register_app_blueprint(configeditor_bp)

def setup(onoapp):
	pass

def start(onoapp):
	pass

def stop(onoapp):
	pass
