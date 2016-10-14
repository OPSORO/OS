import math
import cmath
import time

from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
# from opsoro.stoppable_thread import StoppableThread

from flask import Blueprint, render_template, request

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

config = {"full_name": "Circumplex", "icon": "fa-meh-o", 'color': '#15e678'}

# def CircumplexLoop():
#     while not circumplex_t.stopped():
#         #with Expression.lock:
#         Expression.update()
#
#         circumplex_t.sleep(0.015)
#
#
# circumplex_t = None


def setup_pages(opsoroapp):
    circumplex_bp = Blueprint(
        config['full_name'].lower(),
        __name__,
        template_folder="templates",
        static_folder="static")

    @circumplex_bp.route("/")
    @opsoroapp.app_view
    def index():
        data = {}
        return opsoroapp.render_template(config['full_name'].lower() + ".html",
                                         **data)

    # @circumplex_bp.route("/servos/enable")
    # @opsoroapp.app_api
    # def servosenable():
    #     print_info("Servos enabled")
    #     with Hardware.lock:
    #         Hardware.servo_enable()
    #
    # @circumplex_bp.route("/servos/disable")
    # @opsoroapp.app_api
    # def servosdisable():
    #     print_info("Servos disabled")
    #     with Hardware.lock:
    #         Hardware.servo_disable()

    @circumplex_bp.route("/setemotion", methods=["POST"])
    @opsoroapp.app_api
    def setalphalength():
        phi = request.form.get("phi", type=float, default=0.0)
        r = request.form.get("r", type=float, default=0.0)

        phi = constrain(phi, 0.0, 360.0)
        r = constrain(r, 0.0, 1.0)

        # Set emotion with time -1 for smooth animation based on distance of previous emotion
        #with Expression.lock:
        Expression.set_emotion_r_phi(r, phi, True, -1)
        # Expression is updated in separate thread, no need to do this here.

    opsoroapp.register_app_blueprint(circumplex_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    # Turn servo power off, init servos, update expression
    # with Hardware.lock:
    #     Hardware.servo_disable()
    #     Hardware.servo_init()
    #     Hardware.servo_neutral()

    # with Expression.lock:
    # Neutral emotion
    # Expression.set_emotion_e()
    # Expression.update()

    # Start update thread
    # global circumplex_t
    # circumplex_t = StoppableThread(target=CircumplexLoop)
    # circumplex_t.start()
    pass


def stop(opsoroapp):
    # with Hardware.lock:
    #     Hardware.servo_disable()

    # global circumplex_t
    # if circumplex_t is not None:
    #     circumplex_t.stop()
    pass
