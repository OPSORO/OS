from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, Response
from werkzeug import secure_filename

import math
import cmath

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.expression import Expression

# from opsoro.stoppable_thread import StoppableThread
from opsoro.sound import Sound

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
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


config = {'full_name': 'drive',
          'icon': 'fa-car',
          'color': '#15e678',
          'allowed_background': True,
          'robot_state': 1}

clientconn = None


def setup_pages(opsoroapp):
    app_bp = Blueprint(
        config['full_name'].lower(),
        __name__,
        template_folder="templates",
        static_folder="static")

    @app_bp.route("/", methods=["GET"])
    @opsoroapp.app_view
    def index():
        data = {
            "actions": {},
            "data": [],
        }

        action = request.args.get("action", None)
        if action != None:
            data["actions"][action] = request.args.get("param", None)

        @opsoroapp.app_socket_connected
        def s_connected(conn):
            global clientconn
            clientconn = conn

        @opsoroapp.app_socket_disconnected
        def s_disconnected(conn):
            global clientconn
            clientconn = None

        @opsoroapp.app_socket_message("navUpdate")
        def s_arrow_key(conn, data):
            up = data.pop("up", "")
            down = data.pop("down", "")
            left = data.pop("left", "")
            right = data.pop("right", "")
            instr = arrowKey2motion(up,down,left,right)
            Robot.execute(instr)



        @opsoroapp.app_socket_message("start")
        def s_start(conn,data):
            pass

        @opsoroapp.app_socket_message("stop")
        def s_stop(conn,data):
            pass

        return opsoroapp.render_template(config['full_name'].lower() + ".html",
                                         **data)

    opsoroapp.register_app_blueprint(app_bp)

###############################################################################


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass

def arrowKey2motion(up, down, left , right):
    result = {"action":"stop"}
    if (up & down)  | (left & right):
        result = {"action":"stop","tags":["wheels"]}               #two oposite actions results in no action
    elif up:
        if left:
            result = {"action":"longLeft","tags":["wheels"], "speed":1}             #soft left turn forward
        elif right:
            result = {"action":"longRight","tags":["wheels"], "speed":1}             #soft right turn forward
        else:
            result = {"action":"forward","tags":["wheels"], "speed":1}               #forward
    elif down:
        if left:
            result = {"action":"longLeft","tags":["wheels"], "speed":-1}                #soft left turn backward
        elif right:
            result = {"action":"longRight","tags":["wheels"], "speed":-1}                #soft right turn backward
        else:
            result = {"action":"backward","tags":["wheels"], "speed":1}                #backward
    elif left:
        result = {"action":"shortLeft","tags":["wheels"], "speed":1}                     #hard left turn
    elif right:
        result = {"action":"shortRight","tags":["wheels"], "speed":1}                     #hard right turn
    else:
        result = {"action":"stop","tags":["wheels"]}                        #stand still
    return result
