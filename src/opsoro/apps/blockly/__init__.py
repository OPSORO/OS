from __future__ import with_statement

import glob
import os
from functools import partial

from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug import secure_filename

from opsoro.robot import Robot
from opsoro.users import Users

from ..lua_scripting.scripthost import ScriptHost

config = {
    'full_name':            'Blockly',
    'author':               'OPSORO',
    'icon':                 'fa-puzzle-piece',
    'color':                'blue',
    'difficulty':           3,
    'tags':                 ['visual', 'programming', 'blockly'],
    'allowed_background':   True,
    'multi_user':           False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

sh = None
script = ''
script_name = None
script_modified = False


def add_console(message, color='#888888', icon=None):
    Users.send_app_data(config['formatted_name'], 'addConsole', {'message': message, 'color': color, 'icon': icon})


def send_started():
    Users.send_app_data(config['formatted_name'], 'scriptStarted', {})


def send_stopped():
    Users.send_app_data(config['formatted_name'], 'scriptStopped', {})


def init_ui():
    Users.send_app_data(config['formatted_name'], 'initUI', {})


def ui_add_button(name, caption, icon, toggle=False):
    Users.send_app_data(config['formatted_name'], 'UIAddButton', {'name': name, 'caption': caption, 'icon': icon, 'toggle': toggle})


def ui_add_key(key):
    global sh

    valid_keys = ['up', 'down', 'left', 'right', 'space']
    valid_keys += list('abcdefghijklmnopqrstuvwxyz')
    if key in valid_keys:
        Users.send_app_data(config['formatted_name'], 'UIAddKey', {'key': key})
    else:
        sh.generate_lua_error('Invalid key: %s' % key)


def setup_pages(opsoroapp):
    app_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')

    @app_bp.route('/', methods=['GET'])
    @opsoroapp.app_view
    def index():
        global sh
        global script
        global script_name
        global script_modified

        data = {
            'actions': {},
            'script_name': script_name,
            'script_modified': script_modified,
            'script_running': sh.is_running
        }

        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        if script_name:
            if script_name[-4:] == '.xml' or script_name[-4:] == '.XML':
                data['script_name_noext'] = script_name[:-4]
            else:
                data['script_name_noext'] = script_name

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @app_bp.route('/startscript', methods=['POST'])
    @opsoroapp.app_api
    def startscript():
        global sh
        global script
        global script_name
        global script_modified

        script = request.form.get('luacode', type=str, default='')
        script_xml = request.form.get('xmlcode', type=str, default='')
        script_name = request.form.get('name', type=str, default=None)
        script_modified = request.form.get('modified', type=int, default=0)

        with open(get_path('../../data/' + config['formatted_name'] + '/currentscript.xml.tmp'), 'w') as f:
            f.write(script_xml)

        if sh.is_running:
            sh.stop_script()

        sh.start_script(script)

        return {'status': 'success'}

    @app_bp.route('/stopscript', methods=['POST'])
    @opsoroapp.app_api
    def stopscript():
        global sh

        if sh.is_running:
            sh.stop_script()
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'There is no active script to stop.'}

    @opsoroapp.app_socket_message('keyDown')
    def s_key_down(conn, data):
        global sh

        key = str(data.pop('key', ''))
        sh.ui.set_key_status(key, True)

    @opsoroapp.app_socket_message('keyUp')
    def s_key_up(conn, data):
        global sh

        key = str(data.pop('key', ''))
        sh.ui.set_key_status(key, False)

    @opsoroapp.app_socket_message('buttonDown')
    def s_button_down(conn, data):
        global sh

        button = str(data.pop('button', ''))
        sh.ui.set_button_status(button, True)

    @opsoroapp.app_socket_message('buttonUp')
    def s_button_up(conn, data):
        global sh

        button = str(data.pop('button', ''))
        sh.ui.set_button_status(button, False)

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    global sh
    global script
    global script_name
    global script_modified

    sh = ScriptHost()

    sh.on_print = partial(add_console, color='#888888', icon='fa-info-circle')
    sh.on_error = partial(add_console, color='#ab3226', icon='fa-bug')
    sh.on_start = send_started
    sh.on_stop = send_stopped

    sh.ui.on_init = init_ui
    sh.ui.on_add_button = ui_add_button
    sh.ui.on_add_key = ui_add_key

    script = ''
    script_name = None
    script_modified = False


def stop(opsoroapp):
    global sh
    sh.stop_script()
