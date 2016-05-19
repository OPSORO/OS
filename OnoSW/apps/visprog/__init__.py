from __future__ import with_statement

from functools import partial
import os
import glob
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename
from ..luascripting.scripthost import ScriptHost

config = {"full_name": "Visual Programming", "icon": "fa-puzzle-piece"}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

clientconn = None
sh = None
script = ""
script_name = None
script_modified = False

def add_console(message, color="#888888", icon=None):
	global clientconn
	if clientconn:
		clientconn.send_data("addConsole", {"message": message, "color": color, "icon": icon})

def send_started():
	global clientconn
	if clientconn:
		clientconn.send_data("scriptStarted", {})

def send_stopped():
	global clientconn
	if clientconn:
		clientconn.send_data("scriptStopped", {})

def init_ui():
	global clientconn
	if clientconn:
		clientconn.send_data("initUI", {})

def ui_add_button(name, caption, icon, toggle=False):
	global clientconn
	if clientconn:
		clientconn.send_data("UIAddButton", {"name": name, "caption": caption, "icon": icon, "toggle": toggle})

def ui_add_key(key):
	global clientconn
	global sh
	if clientconn:
		valid_keys = ["up", "down", "left", "right", "space"]
		valid_keys += list("abcdefghijklmnopqrstuvwxyz")
		if key in valid_keys:
			clientconn.send_data("UIAddKey", {"key": key})
		else:
			sh.generate_lua_error("Invalid key: %s" % key)

def setup_pages(opsoroapp):
	visprog_bp = Blueprint("Visual Programming", __name__, template_folder="templates", static_folder="static")

	@visprog_bp.route("/")
	@opsoroapp.app_view
	def index():
		global sh
		global script
		global script_name
		global script_modified

		data = {
			"script_name":		script_name,
			"script_modified":	script_modified,
			"script_running":	sh.is_running
		}

		if script_name:
			if script_name[-4:] == ".xml" or script_name[-4:] == ".XML":
				data["script_name_noext"] = script_name[:-4]
			else:
				data["script_name_noext"] = script_name

		return opsoroapp.render_template("visualprogramming.html", **data)

	@visprog_bp.route("/blockly")
	@opsoroapp.app_view
	def blockly_inner():
		data = {
			"soundfiles":		[]
		}

		filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.wav"))

		for filename in filenames:
			data["soundfiles"].append(os.path.split(filename)[1])

		return opsoroapp.render_template("blockly.html", **data)

	@visprog_bp.route("/filelist")
	@opsoroapp.app_view
	def filelist():
		data = {
			"scriptfiles":	[]
		}

		filenames = []
		filenames.extend(glob.glob(get_path("../../data/visprog/scripts/*.xml")))

		for filename in filenames:
			data["scriptfiles"].append(os.path.split(filename)[1])

		return opsoroapp.render_template("filelist.html", **data)

	@visprog_bp.route("/save", methods=["POST"])
	@opsoroapp.app_api
	def save():
		xmlfile = request.form.get("file", type=str, default="")
		filename = request.form.get("filename", type=str, default="")
		overwrite = request.form.get("overwrite", type=int, default=0)

		if filename == "":
			return {"status": "error", "message": "No filename given."}

		if filename[-4:] != ".xml":
			filename = filename + ".xml"
		filename = secure_filename(filename)

		full_path = os.path.join(get_path("../../data/visprog/scripts/"), filename)

		if overwrite == 0:
			if os.path.isfile(full_path):
				return {"status": "error", "message": "File already exists."}

		with open(full_path, "w") as f:
			f.write(xmlfile)

		return {"status": "success", "filename": filename}

	@visprog_bp.route("/delete/<scriptfile>", methods=["POST"])
	@opsoroapp.app_api
	def delete(scriptfile):
		scriptfiles = []
		filenames = []
		filenames.extend(glob.glob(get_path("../../data/visprog/scripts/*.xml")))
		filenames.extend(glob.glob(get_path("../../data/visprog/scripts/*.XML")))

		for filename in filenames:
			scriptfiles.append(os.path.split(filename)[1])

		if scriptfile in scriptfiles:
			os.remove(os.path.join(get_path("../../data/visprog/scripts/"), scriptfile))
			return {"status": "success", "message": "File %s deleted." % scriptfile}
		else:
			return {"status": "error", "message": "Unknown file."}

	@visprog_bp.route("/scripts/<scriptfile>")
	@opsoroapp.app_view
	def scripts(scriptfile):
		return send_from_directory(get_path("../../data/visprog/scripts/"), scriptfile)

	@visprog_bp.route("/startscript", methods=["POST"])
	@opsoroapp.app_api
	def startscript():
		global sh
		global script
		global script_name
		global script_modified

		script = request.form.get("luacode", type=str, default="")
		script_xml = request.form.get("xmlcode", type=str, default="")
		script_name = request.form.get("name", type=str, default=None)
		script_modified = request.form.get("modified", type=int, default=0)

		with open(get_path("../../data/visprog/scripts/currentscript.xml.tmp"), "w") as f:
			f.write(script_xml)

		if sh.is_running:
			sh.stop_script()

		sh.start_script(script)

		return {"status": "success"}

	@visprog_bp.route("/stopscript", methods=["POST"])
	@opsoroapp.app_api
	def stopscript():
		global sh

		if sh.is_running:
			sh.stop_script()
			return {"status": "success"}
		else:
			return {"status": "error", "message": "There is no active script to stop."}

	@opsoroapp.app_socket_connected
	def s_connected(conn):
		global clientconn
		clientconn = conn

	@opsoroapp.app_socket_disconnected
	def s_disconnected(conn):
		global clientconn
		clientconn = None

	@opsoroapp.app_socket_message("keyDown")
	def s_key_down(conn, data):
		global sh

		key = str(data.pop("key", ""))
		sh.ui.set_key_status(key, True)

	@opsoroapp.app_socket_message("keyUp")
	def s_key_up(conn, data):
		global sh

		key = str(data.pop("key", ""))
		sh.ui.set_key_status(key, False)

	@opsoroapp.app_socket_message("buttonDown")
	def s_button_down(conn, data):
		global sh

		button = str(data.pop("button", ""))
		sh.ui.set_button_status(button, True)

	@opsoroapp.app_socket_message("buttonUp")
	def s_button_up(conn, data):
		global sh

		button = str(data.pop("button", ""))
		sh.ui.set_button_status(button, False)

	opsoroapp.register_app_blueprint(visprog_bp)

def setup(opsoroapp):
	pass

def start(opsoroapp):
	global sh
	global script
	global script_name
	global script_modified

	sh = ScriptHost()

	sh.on_print = partial(add_console, color="#888888", icon="fa-info-circle")
	sh.on_error = partial(add_console, color="#ab3226", icon="fa-bug")
	sh.on_start = send_started
	sh.on_stop = send_stopped

	sh.ui.on_init = init_ui
	sh.ui.on_add_button = ui_add_button
	sh.ui.on_add_key = ui_add_key

	script = ""
	script_name = None
	script_modified = False

def stop(opsoroapp):
	global sh
	sh.stop_script()
