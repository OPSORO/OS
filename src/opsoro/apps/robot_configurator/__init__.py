from __future__ import with_statement

import glob
import os
from functools import partial

import yaml
from flask import Blueprint, render_template, request

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


config = {
    'full_name':            'Robot Configurator',
    'author':               'OPSORO',
    'icon':                 'fa-pencil',
    'color':                'red',
    'difficulty':           3,
    'tags':                 ['design', 'setup', 'robot', 'configuration'],
    'allowed_background':   False,
    'multi_user':           False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO_NOT_ALIVE,
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


def setup_pages(opsoroapp):
    app_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @app_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        data = {
            'actions': {},
            'data': [],
            'modules': [],
            'svg_codes': {},
            'configs': {},
            'specs': {},
            'skins': [],
        }

        data['actions']['openfile'] = request.args.get('f', None)

        modules_folder = '../../modules/'
        modules_static_folder = '../../server/static/modules/'

        # get modules
        filenames = []
        filenames.extend(glob.glob(get_path(modules_folder + '*/')))
        for filename in filenames:
            module_name = filename.split('/')[-2]
            data['modules'].append(module_name)
            with open(get_path(modules_folder + module_name + '/specs.yaml')) as f:
                data['specs'][module_name] = yaml.load(f, Loader=Loader)

            with open(get_path(modules_static_folder + module_name + '/front.svg')) as f:
                data['svg_codes'][module_name] = f.read()

        data['configs'] = Robot.config

        # filenames = []
        # filenames.extend(glob.glob(get_path('static/images/skins/*.svg')))
        # for filename in filenames:
        #     data['skins'].append(os.path.splitext(os.path.split(filename)[1])[0])

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @opsoroapp.app_socket_message('setServoPos')
    def s_setServoPos(conn, data):
        pin = constrain(int(data.pop('pin', None)), 0, 15)
        value = constrain(int(data.pop('value', None)), 500, 2500)

        if pin is None or value is None:
            conn.send_data('error', {'message': 'No valid pin or value given.'})
            return

        Hardware.Servo.set(pin, value)

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
