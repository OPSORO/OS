from __future__ import with_statement

import glob
import os
from functools import partial

import yaml
from flask import Blueprint, render_template, request

from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.robot import Robot

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


config = {
    'full_name':            'Expression Configurator',
    'author':               'OPSORO',
    'icon':                 'fa-smile-o',
    'color':                'red',
    'difficulty':           3,
    'tags':                 ['design', 'setup', 'expression', 'configuration'],
    'allowed_background':   False,
    'multi_user':           True,
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
            'expressions': {},
            'icons': [],
        }

        # action = request.args.get('action', None)
        # if action != None:
        data['actions']['openfile'] = request.args.get('f', None)

        modules_folder = '../../modules/'
        modules_static_folder = '../../server/static/modules/'
        icons_static_folder = '../../server/static/images/emojione/'

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
        data['expressions'] = Expression.expressions

        filenames = []
        filenames.extend(glob.glob(get_path(icons_static_folder + '*.svg')))
        for filename in filenames:
            data['icons'].append(os.path.splitext(os.path.split(filename)[1])[0])

        # filenames = []
        # filenames.extend(glob.glob(get_path('static/images/skins/*.svg')))
        # for filename in filenames:
        #     data['skins'].append(os.path.splitext(os.path.split(filename)[1])[0])

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @opsoroapp.app_socket_message('setDofs')
    def s_setDofs(conn, data):
        dof_values = data.pop('dofs', None)

        if dof_values is None:
            conn.send_data('error', {'message': 'No valid pin or value given.'})
            return

        if type(dof_values) is dict:
            Robot.set_dof_values(dof_values)
        elif type(dof_values) is list:
            Robot.set_dof_list(dof_values)

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
