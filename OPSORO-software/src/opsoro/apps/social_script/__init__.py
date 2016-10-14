from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename
from opsoro.sound import Sound

import math
import cmath

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.stoppable_thread import StoppableThread

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

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

from opsoro.expression import Expression

config = {"full_name": "Social_Script",
          "icon": "fa-commenting-o",
          'color': '#15e678'}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

dof_positions = {}

clientconn = None


def send_stopped():
    global clientconn
    if clientconn:
        clientconn.send_data("soundStopped", {})

# def SocialscriptLoop():
#     while not socialscriptloop_t.stopped():
#         # with Expression.lock:
#         Expression.update()
#
#         socialscriptloop_t.sleep(0.015)


def SocialscriptRun():
    Sound.wait_for_sound()
    send_stopped()

# socialscriptloop_t = None
socialscript_t = None


def setup_pages(opsoroapp):
    socialscript_bp = Blueprint(
        config['full_name'].lower(),
        __name__,
        template_folder="templates",
        static_folder="static")

    @socialscript_bp.route("/", methods=["GET"])
    @opsoroapp.app_view
    def index():
        data = {"actions": {}, "emotions": [], "sounds": []}

        action = request.args.get("action", None)
        if action != None:
            data["actions"][action] = request.args.get("param", None)

        with open(get_path("emotions.yaml")) as f:
            data["emotions"] = yaml.load(f, Loader=Loader)

        filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.wav"))

        for filename in filenames:
            data["sounds"].append(os.path.split(filename)[1])
        data["sounds"].sort()

        return opsoroapp.render_template(config['full_name'].lower() + ".html",
                                         **data)

    @opsoroapp.app_socket_connected
    def s_connected(conn):
        global clientconn
        clientconn = conn

    @opsoroapp.app_socket_disconnected
    def s_disconnected(conn):
        global clientconn
        clientconn = None

    @socialscript_bp.route("/setemotion", methods=["POST"])
    @opsoroapp.app_api
    def setemotion():
        phi = request.form.get("phi", type=float, default=0.0)
        r = request.form.get("r", type=float, default=0.0)

        phi = constrain(phi, 0.0, 360.0)
        r = constrain(r, 0.0, 1.0)

        # with Expression.lock:
        Expression.set_emotion_r_phi(r, phi, True, 0.5)

    @socialscript_bp.route("/play/<soundfile>", methods=["GET"])
    @opsoroapp.app_api
    def play(soundfile):
        soundfiles = []
        filenames = []

        filenames = glob.glob(get_path("../../data/sounds/soundfiles/*.wav"))

        for filename in filenames:
            soundfiles.append(os.path.split(filename)[1])

        if soundfile in soundfiles:
            Sound.play_file(soundfile)

            global socialscript_t
            if socialscript_t != None:
                socialscript_t.stop()
            socialscript_t = StoppableThread(target=SocialscriptRun)

            return {"status": "success"}

        else:
            return {"status": "error", "message": "Unknown file."}

    @socialscript_bp.route("/stopsound", methods=["GET"])
    @opsoroapp.app_api
    def stopsound():
        # Sound.say_tts("")
        Sound.stop_sound()
        global socialscript_t
        if socialscript_t != None:
            socialscript_t.stop()
        return {"status": "success"}

    @socialscript_bp.route("/saytts", methods=["GET"])
    @opsoroapp.app_api
    def saytts():
        text = request.args.get("text", None)
        if text is not None:
            Sound.say_tts(text)

            global socialscript_t
            if socialscript_t != None:
                socialscript_t.stop()
            socialscript_t = StoppableThread(target=SocialscriptRun)

        return {"status": "success"}

    @socialscript_bp.route("/setDofData", methods=["POST"])
    @opsoroapp.app_api
    def s_setdofpos():
        global dof_positions

        dofdata = yaml.load(
            request.form.get("dofdata", type=str, default=""), Loader=Loader)
        #dofdata = json.loads(request.form.get("dofdata", type=str, default=""))

        # Expression.set_dof_values(dofdata)
        #print dofdata("m_l")
        #
        # for dof in dofdata:
        # 	dofdata[dof] = constrain(dofdata[dof], -1.0, 1.0)
        #
        # print dofdata
        # print Expression.dof_values
        # print Expression.dofs
        # dof_positions = dofdata;
        # Expression.dofs = dof_positions
        # print Expression.dofs

        # with Expression.lock:
        # 	Expression.update()

        return {"status": "success"}

    opsoroapp.register_app_blueprint(socialscript_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    # Apply overlay function
    # for servo in Expression.servos:
    #     if servo.pin < 0 or servo.pin > 15:
    #         continue  # Skip invalid pins
    #     dof_positions[servo.dofname] = 0.0

    # # Turn servo power off, init servos, update expression
    # with Hardware.lock:
    #     Hardware.servo_disable()
    #     Hardware.servo_init()
    #     Hardware.servo_neutral()

    # with Expression.lock:
    # Expression.set_emotion_e()
    # Expression.update()

    # # Start update thread
    # global socialscriptloop_t
    # socialscriptloop_t = StoppableThread(target=SocialscriptLoop)
    # socialscriptloop_t.start()
    pass


def stop(opsoroapp):
    # with Hardware.lock:
    #     Hardware.servo_disable()
    #
    # global socialscriptloop_t
    # if socialscriptloop_t is not None:
    #     socialscriptloop_t.stop()
    # if socialscript_t is not None:
    #     socialscript_t.stop()
    pass
