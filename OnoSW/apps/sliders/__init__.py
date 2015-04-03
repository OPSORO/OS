from __future__ import with_statement

import os
import threading
import time
from functools import partial
from stoppable_thread import StoppableThread
from expression_manager import ExpressionManager

from flask import Blueprint, render_template, request, redirect, url_for, flash

config = {"full_name": "Sliders", "icon": "fa-sliders"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

em = None
em_lock = threading.Lock()

def setup_pages(onoapp):
	sliders_bp = Blueprint("sliders", __name__, template_folder="templates")

	@sliders_bp.route("/")
	@onoapp.app_view
	def index():
		data = {
			"page_icon":		config["icon"],
			"page_caption":		config["full_name"],
			"title":			"Ono web interface - %s" % config["full_name"],
			"dofs":				[]
		}

		global em

		for pin, pinname in enumerate(em.pinmap):
			if pinname is not None:
				data["dofs"].append({
					"name":		pinname,
					"pin":		pin,
					"min":		em.dof[pinname].min_range,
					"mid":		em.dof[pinname].mid_pos,
					"max":		em.dof[pinname].max_range,
					"current":	em.dof[pinname].pos_current
				})

		return onoapp.render_template("sliders.html", **data)

	@sliders_bp.route("/servos/enable")
	@onoapp.app_api
	def servosenable():
		print "\033[93m" + "Servos now on" + "\033[0m"
		onoapp.hw.servo_power_on()

	@sliders_bp.route("/servos/disable")
	@onoapp.app_api
	def servosdisable():
		print "\033[93m" + "Servos now off" + "\033[0m"
		onoapp.hw.servo_power_off()

	@sliders_bp.route("/setdofpos", methods=["POST"])
	@onoapp.app_api
	def setdofpos():
		dofname = request.form.get("dof", type=str, default=None)
		pos = request.form.get("pos", type=int, default=0)

		if dofname is None:
			return {"status": "error", "message": "No DOF name given."}
		if dofname not in em.pinmap:
			return {"status": "error", "message": "Unknown DOF name."}

		global em
		global em_lock

		with em_lock:
			em.dof[dofname].set_target_pos(pos=pos, steps=0)
			em.update_servos()

	onoapp.register_app_blueprint(sliders_bp)

def setup(onoapp):
	global em
	global em_lock
	with em_lock:
		em = ExpressionManager(onoapp.hw)
		em.all_servos_mid()

def start(onoapp):
	pass

def stop(onoapp):
	onoapp.hw.servo_power_off()
