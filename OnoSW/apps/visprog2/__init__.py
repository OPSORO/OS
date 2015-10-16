from __future__ import with_statement

from functools import partial
import os
import glob
from flask import Blueprint, render_template, request, redirect, url_for, flash

config = {"full_name": "VisProg2", "icon": "fa-puzzle-piece"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

def setup_pages(onoapp):
	visprog2_bp = Blueprint("visprog2", __name__, template_folder="templates", static_folder="static")

	@visprog2_bp.route("/")
	@onoapp.app_view
	def index():
		data = {
			"page_icon":		config["icon"],
			"page_caption":		config["full_name"],
			"title":			"Ono web interface - %s" % config["full_name"],
		}

		return onoapp.render_template("visualprogramming.html", **data)

	@visprog2_bp.route("/blockly")
	@onoapp.app_view
	def blockly_inner():
		data = {
			"soundfiles":		[]
		}

		filenames = glob.glob(get_path("../sounds/soundfiles/*.wav"))

		for filename in filenames:
			data["soundfiles"].append(os.path.split(filename)[1])

		return onoapp.render_template("blockly.html", **data)

	onoapp.register_app_blueprint(visprog2_bp)

def setup(onoapp):
	pass

def start(onoapp):
	pass

def stop(onoapp):
	pass
