from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename

from opsoro.console_msg import *
from opsoro.hardware import Hardware
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

config = {
    'full_name':            'Expression Configurator',
    'icon':                 'fa-smile-o',
    'color':                'red',
    'difficulty':           3,
    'tags':                 ['design', 'setup', 'expression', 'configuration'],
    'allowed_background':   False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.MANUAL
}
config['formatted_name'] =  config['full_name'].lower().replace(' ', '_')

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))


def setup_pages(opsoroapp):
    app_bp = Blueprint(
        config['formatted_name'],
        __name__,
        template_folder='templates',
        static_folder='static')

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

        # with open(get_path('../../config/modules_configs/ono.yaml')) as f:
        # 	data['config'] = yaml.load(f, Loader=Loader)
        #
        modules_folder = '../../modules/'
        modules_static_folder = '../../server/static/modules/'
        icons_static_folder = '../../server/static/images/emojione/'
        config_folder = '../../config/'

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

        with open(get_path(config_folder + 'new_grid.yaml')) as f:
            data['configs'] = yaml.load(f, Loader=Loader)['modules']
        with open(get_path(config_folder + 'default_expressions.yaml')) as f:
            data['expressions'] = yaml.load(f, Loader=Loader)['expressions']

        filenames = []
        filenames.extend(glob.glob(get_path(icons_static_folder + '*.svg')))
        for filename in filenames:
            data['icons'].append(os.path.splitext(os.path.split(filename)[1])[0])

        # filenames = []
        # filenames.extend(glob.glob(get_path('static/images/skins/*.svg')))
        # for filename in filenames:
        #     data['skins'].append(os.path.splitext(os.path.split(filename)[1])[0])

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
