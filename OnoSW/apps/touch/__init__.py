from __future__ import with_statement
from __future__ import division

import threading
import random
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash
from stoppable_thread import StoppableThread
from hardware import Hardware

config = {"full_name": "Touch Graph", "icon": "fa-hand-o-down"}

touch_t = None
clientconn = None
running = False
numelectrodes = 0

def TouchLoop():
	global running
	global clientconn

	while not touch_t.stopped():
		if running:
			data = {}

			with Hardware.lock:
				ret = Hardware.cap_get_filtered_data()

			for i in range(numelectrodes):
				data[i] = ret[i]

			if clientconn:
				clientconn.send_data("updateelectrodes", {"electrodedata": data})

		touch_t.sleep(0.1)

def startcap(electrodes):
	global running
	global numelectrodes

	Hardware.cap_init(electrodes=electrodes, gpios=0, autoconfig=True)
	numelectrodes = electrodes

	running = True

def stopcap():
	global running
	running = False

def setup_pages(onoapp):
	touch_bp = Blueprint("touch", __name__, template_folder="templates")

	@touch_bp.route("/")
	@onoapp.app_view
	def index():
		data = {
			"page_icon":		config["icon"],
			"page_caption":		config["full_name"],
			"title":			"Ono web interface - %s" % config["full_name"],
		}

		return onoapp.render_template("touch.html", **data)

	@onoapp.app_socket_connected
	def s_connected(conn):
		global clientconn
		clientconn = conn

	@onoapp.app_socket_disconnected
	def s_disconnected(conn):
		global clientconn
		clientconn = None

	@onoapp.app_socket_message("startcapture")
	def s_startcapture(conn, data):
		electrodes = int(data.pop("electrodes", 0))
		startcap(electrodes)

	@onoapp.app_socket_message("stopcapture")
	def s_stopcapture(conn, data):
		stopcap()

	onoapp.register_app_blueprint(touch_bp)

def setup(onoapp):
	pass

def start(onoapp):
	global touch_t

	touch_t = StoppableThread(target=TouchLoop)
	touch_t.start();

def stop(onoapp):
	global touch_t
	global running

	running = False
	touch_t.stop()
