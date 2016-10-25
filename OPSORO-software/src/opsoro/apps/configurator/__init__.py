from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename

# import math
# import cmath

from opsoro.console_msg import *
from opsoro.hardware import Hardware
# from opsoro.stoppable_thread import StoppableThread
# from opsoro.sound import Sound
from opsoro.robot import Robot

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

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

config = {"full_name": "Configurator", "icon": "fa-pencil", 'color': '#ff517e'}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


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
            "modules": [],
            "skins": [],
        }

        # action = request.args.get("action", None)
        # if action != None:
        data['actions']['openfile'] = request.args.get("f", None)

        # with open(get_path("../../config/modules_configs/ono.yaml")) as f:
        # 	data["config"] = yaml.load(f, Loader=Loader)
        #
        filenames = []

        filenames.extend(glob.glob(get_path("static/images/*.svg")))
        for filename in filenames:
            data["modules"].append(
                os.path.splitext(os.path.split(filename)[1])[0])

        filenames = []

        filenames.extend(glob.glob(get_path("static/images/skins/*.svg")))
        for filename in filenames:
            data["skins"].append(
                os.path.splitext(os.path.split(filename)[1])[0])

        return opsoroapp.render_template(config['full_name'].lower() + ".html",
                                         **data)

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
