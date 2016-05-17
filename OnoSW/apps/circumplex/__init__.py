import math
import cmath
import time

from console_msg import *
from expression import Expression
from hardware import Hardware
from stoppable_thread import StoppableThread

from flask import Blueprint, render_template, request

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

config = {"full_name": "Circumplex Interface", "icon": "fa-meh-o"}

def CircumplexLoop():
	while not circumplex_t.stopped():
		with Expression.lock:
			Expression.update()

		circumplex_t.sleep(0.015)

circumplex_t = None

def setup_pages(opsoroapp):
	circumplex_bp = Blueprint("circumplex", __name__, template_folder="templates", static_folder="static")

	@circumplex_bp.route("/")
	@opsoroapp.app_view
	def index():
		data = {
		}
		return opsoroapp.render_template("circumplex.html", **data)

	@circumplex_bp.route("/servos/enable")
	@opsoroapp.app_api
	def servosenable():
		print_info("Servos enabled")
		with Hardware.lock:
			Hardware.servo_enable()

	@circumplex_bp.route("/servos/disable")
	@opsoroapp.app_api
	def servosdisable():
		print_info("Servos disabled")
		with Hardware.lock:
			Hardware.servo_disable()

	@circumplex_bp.route("/setemotion", methods=["POST"])
	@opsoroapp.app_api
	def setalphalength():
		phi = request.form.get("phi", type=float, default=0.0)
		r = request.form.get("r", type=float, default=0.0)

		phi = constrain(phi, 0.0, 360.0)
		r = constrain(r, 0.0, 1.0)

		phi = phi * math.pi/180.0

		# Calculate distance between old and new emotions.
		# Shorter emotional distances are animated faster than longer distances.
		e_old = Expression.get_emotion_complex()
		e_new = cmath.rect(r, phi)
		dist = abs(e_new - e_old)

		with Expression.lock:
			Expression.set_emotion(phi=phi, r=r, anim_time=dist)
			# Expression is updated in separate thread, no need to do this here.

	opsoroapp.register_app_blueprint(circumplex_bp)


def setup(opsoroapp):
	pass

def start(opsoroapp):
	# Turn servo power off, init servos, update expression
	with Hardware.lock:
		Hardware.servo_disable()
		Hardware.servo_init()
		Hardware.servo_neutral()

	with Expression.lock:
		Expression.set_emotion(valence=0.0, arousal=0.0)
		Expression.update()

	# Start update thread
	global circumplex_t
	circumplex_t = StoppableThread(target=CircumplexLoop)
	circumplex_t.start();

def stop(opsoroapp):
	with Hardware.lock:
		Hardware.servo_disable()

	global circumplex_t
	if circumplex_t is not None:
		circumplex_t.stop()
