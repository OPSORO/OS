from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename

import math
import cmath

from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.Camera import Camera
# from opsoro.stoppable_thread import StoppableThread


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

config = {"full_name": "webcam", "icon": "fa-video-camera", 'color': '#15e678'}

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

        return opsoroapp.render_template(config['full_name'].lower() + ".html",
                                         **data)


    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    Camera.startInternetStream()

def stop(opsoroapp):
    Camera.stopInternetStream()
