from __future__ import with_statement

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

from expression import Expression

config = {"full_name": "Social Script", "icon": "fa-commenting-o"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

def setup_pages(onoapp):
	socialscript_bp = Blueprint("socialscript", __name__, template_folder="templates", static_folder="static")

	@socialscript_bp.route("/")
	@onoapp.app_view
	def index():
		data = {
			"page_icon":		config["icon"],
			"page_caption":		config["full_name"],
			"title":			"Ono web interface - %s" % config["full_name"],
			"emotions":			[],
			"sounds":			[]
		}

		with open(get_path("emotions.yaml")) as f:
			data["emotions"] = yaml.load(f, Loader=Loader)

		filenames = glob.glob(get_path("../sounds/soundfiles/*.wav"))

		for filename in filenames:
			data["sounds"].append(os.path.split(filename)[1])
		data["sounds"].sort()

		return onoapp.render_template("socialscript.html", **data)

	onoapp.register_app_blueprint(socialscript_bp)

def setup(onoapp):
	pass

def start(onoapp):
	pass

def stop(onoapp):
	pass
