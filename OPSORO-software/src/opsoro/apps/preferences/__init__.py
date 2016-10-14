from __future__ import with_statement

from opsoro.console_msg import *
# from opsoro.robot import Robot
# from opsoro.hardware import Hardware
from opsoro.preferences import Preferences

from flask import Blueprint, render_template, request, redirect, url_for, flash

# constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

config = {'full_name': 'Preferences', 'icon': 'fa-cog', 'color': '#555'}

# clientconn = None
# dof_positions = {}

# import os
# from functools import partial

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def setup_pages(opsoroapp):
    app_bp = Blueprint(
        config['full_name'].lower(),
        __name__,
        template_folder='templates',
        static_folder='static')

    global clientconn

    @app_bp.route('/', methods=["GET", "POST"])
    @opsoroapp.app_view
    def index():
        data = {}
        if request.method == 'POST':
            # Update preferences
            Preferences.set('general', 'robot_name', request.form['robotName'])

            if request.form['robotPassword'] == request.form[
                    'robotPasswordConfirm']:
                if request.form['robotPassword'] != '':
                    Preferences.set('general', 'password',
                                    request.form['robotPassword'])

            Preferences.set('audio',
                            'master_volume',
                            request.form.get('volume', type=int))
            Preferences.set('audio', 'tts_engine', request.form['ttsEngine'])
            Preferences.set('audio', 'tts_language',
                            request.form['ttsLanguage'])
            Preferences.set('audio', 'tts_gender', request.form['ttsGender'])

            Preferences.set('wireless', 'ssid', request.form['wirelessSsid'])
            Preferences.set('wireless',
                            'channel',
                            request.form.get('wirelessChannel', type=int))

            if request.form.get('wirelessSamePass', None) == 'on':
                # Set to same password
                Preferences.set('wireless', 'password', Preferences.get(
                    'general', 'password', 'RobotOpsoro'))
            else:
                if request.form['wirelessPassword'] == request.form[
                        'wirelessPasswordConfirm']:
                    if request.form['wirelessPassword'] != '':
                        Preferences.set('wireless', 'password',
                                        request.form['wirelessPassword'])

            flash('Preferences have been saved.', 'success')
            Preferences.save_prefs()
            Preferences.apply_prefs(
                update_audio=True,
                update_wireless=True,
                restart_wireless=False)

        # Prepare json string with prefs data
        data['prefs'] = {
            'general': {
                'robotName':
                Preferences.get('general', 'robot_name', 'Robot')
            },
            'audio': {
                'volume': Preferences.get('audio', 'master_volume', 66),
                'ttsEngine': Preferences.get('audio', 'tts_engine', 'pico'),
                'ttsLanguage': Preferences.get('audio', 'tts_language', 'nl'),
                'ttsGender': Preferences.get('audio', 'tts_gender', 'm')
            },
            'wireless': {
                'ssid':
                Preferences.get('wireless', 'ssid', 'OPSORO' + '_AP'),
                'samePassword':
                Preferences.get('general', 'password', 'RobotOpsoro') ==
                Preferences.get('wireless', 'password', 'RobotOpsoro'),
                'channel': Preferences.get('wireless', 'channel', '1')
            }
        }

        return opsoroapp.render_template(config['full_name'].lower() + '.html',
                                         **data)

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
