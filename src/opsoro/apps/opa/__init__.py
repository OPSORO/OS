from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.expression import Expression
# from opsoro.stoppable_thread import StoppableThread
from opsoro.sound import Sound

from functools import partial
import os

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

config = {
    'full_name':            'Opsoro Personal Assistant',
    'icon':                 'fa-hand-spock-o',
    'color':                'green',
    'difficulty':           1,
    'tags':                 ['template', 'developer'],
    'allowed_background':   False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] =  config['full_name'].lower().replace(' ', '_')

def setup_pages(server):
    app_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    # Public function declarations
    app_bp.add_url_rule('/demo',    'demo',     server.app_api(demo),       methods=['GET', 'POST'])

    @app_bp.route('/')
    @server.app_view
    def index():
        data = {
            'actions': {},
            'data': [],
        }
        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        return server.render_template(config['formatted_name'] + '.html', **data)

    server.register_app_blueprint(app_bp)

def demo():
    # publicly accessible function
    if 1 > 0:
        return {'status': 'success'}
    else:
        return {'status': 'error', 'message': 'This is a demo error!'}

# Default functions for setting up, starting and stopping an app
def setup(server):
    pass

def start(server):
    pass

def stop(server):
    pass
