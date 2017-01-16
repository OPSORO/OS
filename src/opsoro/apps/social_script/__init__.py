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

# from opsoro.expression import Expression

config = {'full_name': 'Social Script',
          'icon': 'fa-commenting-o',
          'color': '#15e678',
          'allowed_background': False,
          'robot_state': 1}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

# robot_state:
# 0: Manual start/stop
# 1: Start robot automatically (alive feature according to preferences)
# 2: Start robot automatically and enable alive feature
# 3: Start robot automatically and disable alive feature

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

dof_positions = {}

clientconn = None


def send_stopped():
    global clientconn
    if clientconn:
        clientconn.send_data('soundStopped', {})


def SocialscriptRun():
    Sound.wait_for_sound()
    send_stopped()


socialscript_t = None


def setup_pages(opsoroapp):
    socialscript_bp = Blueprint(
        config['formatted_name'],
        __name__,
        template_folder='templates',
        static_folder='static')

    @socialscript_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {'actions': {}, 'emotions': [], 'sounds': []}

        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        with open(get_path('emotions.yaml')) as f:
            data['emotions'] = yaml.load(f, Loader=Loader)

        filenames = glob.glob(get_path('../../data/sounds/*.wav'))

        for filename in filenames:
            data['sounds'].append(os.path.split(filename)[1])
        data['sounds'].sort()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @opsoroapp.app_socket_connected
    def s_connected(conn):
        global clientconn
        clientconn = conn

    @opsoroapp.app_socket_disconnected
    def s_disconnected(conn):
        global clientconn
        clientconn = None

    opsoroapp.register_app_blueprint(socialscript_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
