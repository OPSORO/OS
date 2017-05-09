from __future__ import with_statement

from flask import Blueprint, flash, redirect, render_template, request, url_for

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


config = {
    'full_name':            'Cockpit',
    'author':               'OPSORO',
    'icon':                 'fa-rocket',
    'color':                'red',
    'difficulty':           9,
    'tags':                 [''],
    'allowed_background':   False,
    'multi_user':           False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')


def setup_pages(opsoroapp):
    app_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @app_bp.route('/')
    @opsoroapp.app_view
    def index():
        data = {
            # 'dofs':				[]
        }
        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

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
