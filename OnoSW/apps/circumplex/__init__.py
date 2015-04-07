import os
import threading
from functools import partial
from flask import Blueprint, render_template, request
from stoppable_thread import StoppableThread
from expression_manager import ExpressionManager

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

def constrain(n, minn, maxn):
	if n < minn:
		return minn
	elif n > maxn:
		return maxn
	else:
		return n

config = {"full_name": "Circumplex Interface", "icon": "fa-meh-o"}

def CircumplexLoop():
	while not circumplex_t.stopped():
		global em
		global em_lock
		with em_lock:
			em.step()
			em.update_servos()
		circumplex_t.sleep(0.01)

circumplex_t = None
em = None
em_lock = threading.Lock()

alpha = 0.0
length = 0.0

def setup_pages(onoapp):
	circumplex_bp = Blueprint("circumplex", __name__, template_folder="templates", static_folder="static")

	global em
	global em_lock

	global alpha
	global length

	@circumplex_bp.route("/")
	@onoapp.app_view
	def index():
		data = {
			"page_icon":		config["icon"],
			"page_caption":		config["full_name"],
			"page_content":		"Hello from the circumplex app: Circumplex Index",
			"title":			"Ono web interface - %s" % config["full_name"]
		}
		return onoapp.render_template("circumplex.html", **data)

	@circumplex_bp.route("/servos/enable")
	@onoapp.app_api
	def servosenable():
		print "\033[93m" + "Servos now on" + "\033[0m"

		with em_lock:
			em.parse_configs()
			em.set_target_alpha_length(alpha, length)

		onoapp.hw.servo_power_on()

	@circumplex_bp.route("/servos/disable")
	@onoapp.app_api
	def servosdisable():
		print "\033[93m" + "Servos now off" + "\033[0m"
		onoapp.hw.servo_power_off()

	@circumplex_bp.route("/setalphalength", methods=["POST"])
	@onoapp.app_api
	def setalphalength():
		alpha_new = request.form.get("alpha", type=float, default=0.0)
		length_new = request.form.get("length", type=float, default=0.0)

		alpha_new = constrain(alpha_new, 0.0, 360.0)
		length_new = constrain(length_new, 0.0, 1.0)

		alpha = alpha_new
		length = length_new

		with em_lock:
			em.set_target_alpha_length(alpha, length, steps=25)
			em.update_servos()

	onoapp.register_app_blueprint(circumplex_bp)


def setup(onoapp):
	global em
	global em_lock
	with em_lock:
		em = ExpressionManager(onoapp.hw)
		em.all_servos_mid()

def start(onoapp):
	global circumplex_t
	circumplex_t = StoppableThread(target=CircumplexLoop)
	circumplex_t.start();

def stop(onoapp):
	global circumplex_t
	circumplex_t.stop()
