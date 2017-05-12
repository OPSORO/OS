from __future__ import with_statement

import os
from functools import partial

import yaml
from flask import Blueprint, flash, redirect, render_template, request, url_for

from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


config = {
    'full_name':            'Sliders',
    'author':               'OPSORO',
    'icon':                 'fa-sliders',
    'color':                'gray_light',
    'difficulty':           2,
    'tags':                 ['sliders', 'dofs'],
    'allowed_background':   False,
    'multi_user':           False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

# dof_positions = {}

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def setup_pages(opsoroapp):
    sliders_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @sliders_bp.route('/')
    @opsoroapp.app_view
    def index():
        data = {
            # 'dofs':				[]
        }

        data['config'] = Robot.config['modules']

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @opsoroapp.app_socket_message('setDofPos')
    def s_setdofpos(conn, data):
        modulename = str(data.pop('module_name', None))
        dofname = str(data.pop('dof_name', None))
        pos = float(data.pop('pos', 0.0))

        if modulename is None or dofname is None:
            conn.send_data('error', {'message': 'No valid dof name given.'})
            return

        Robot.set_dof_value(modulename, dofname, pos, 0)

    opsoroapp.register_app_blueprint(sliders_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
