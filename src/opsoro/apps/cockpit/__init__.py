from __future__ import with_statement

from opsoro.console_msg import *
from opsoro.robot import Robot
from opsoro.hardware import Hardware

from flask import Blueprint, render_template, request, redirect, url_for, flash

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

config = {
    'full_name':            'Cockpit',
    'icon':                 'fa-rocket',
    'color':                '#ff517e',
    'difficulty':           9,
    'tags':                 [''],
    'allowed_background':   False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] =  config['full_name'].lower().replace(' ', '_')

clientconn = None

# dof_positions = {}

# import os

# import yaml
# try:
#     from yaml import CLoader as Loader
# except ImportError:
#     from yaml import Loader


def setup_pages(opsoroapp):
    app_bp = Blueprint(
        config['formatted_name'],
        __name__,
        template_folder='templates',
        static_folder='static')

    global clientconn

    @app_bp.route('/')
    @opsoroapp.app_view
    def index():
        data = {
            # 'dofs':				[]
        }

        # global dof_positions
        #
        # for servo in Expression.servos:
        # 	if servo.pin >= 0 and servo.pin < 16:
        # 		# Pin is valid, add to the page
        # 		data['dofs'].append({
        # 			'name':		servo.dofname,
        # 			'pin':		servo.pin,
        # 			'min':		servo.min_range,
        # 			'mid':		servo.mid_pos,
        # 			'max':		servo.max_range,
        # 			'current':	dof_positions[servo.dofname]
        # 		})

        # with open(get_path('../../config/default.conf')) as f:
        #     data['config'] = yaml.load(f, Loader=Loader)

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @opsoroapp.app_socket_connected
    def s_connected(conn):
        global clientconn
        clientconn = conn

    @opsoroapp.app_socket_disconnected
    def s_disconnected(conn):
        global clientconn
        clientconn = None

    @opsoroapp.app_socket_message('setServoPos')
    def s_setservopos(conn, data):
        pin_number = int(data.pop('pin_number', 0))
        value = int(data.pop('value', 1500))

        value = constrain(value, 500, 2500)

        with Hardware.lock:
            Hardware.Servo.set(pin_number, value)

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):

    pass


def stop(opsoroapp):
    pass
