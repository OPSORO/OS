from __future__ import with_statement

import glob
import math
import os
import shutil
import time
from exceptions import RuntimeError
from functools import partial

import yaml
from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug import secure_filename

import cmath
from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def constrain(n, minn, maxn): return max(min(maxn, n), minn)

# from opsoro.expression import Expression


config = {
    'full_name':            'Social Script',
    'author':               'OPSORO',
    'icon':                 'fa-commenting-o',
    'color':                'orange',
    'difficulty':           4,
    'tags':                 [''],
    'allowed_background':   False,
    'multi_user':           True,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

dof_positions = {}


def send_stopped():
    Users.send_app_data(config['formatted_name'], 'soundStopped', {})


def SocialscriptRun():
    Sound.wait_for_sound()
    send_stopped()


socialscript_t = None


def setup_pages(opsoroapp):
    socialscript_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @socialscript_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {'actions': {}, 'emotions': [], 'sounds': []}

        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        data['emotions'] = Expression.expressions

        filenames = glob.glob(get_path('../../data/sounds/*.wav'))

        for filename in filenames:
            data['sounds'].append(os.path.split(filename)[1])
        data['sounds'].sort()

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    opsoroapp.register_app_blueprint(socialscript_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
