from __future__ import with_statement

from opsoro.console_msg import *
from opsoro.robot import Robot
# from opsoro.hardware import Hardware
from opsoro.preferences import Preferences

from flask import Blueprint, render_template, request, redirect, url_for, flash

# constrain = lambda n, minn, maxn: max(min(maxn, n), minn)

config = {'full_name': 'Preferences',
          'icon': 'fa-cog',
          'color': '#555',
          'allowed_background': False,
          'connection': Robot.Connection.OFFLINE,
          'activation': Robot.Activation.MANUAL}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

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
        config['formatted_name'],
        __name__,
        template_folder='templates',
        static_folder='static')

    global clientconn

    @app_bp.route('/', methods=['GET', 'POST'])
    @opsoroapp.app_view
    def index():
        data = {}
        if request.method == 'POST':
            # Update preferences
            request.form.get('file_name_ext', type=str, default=None)
            Preferences.set('general',
                            'robot_name',
                            request.form.get('robotName',
                                             type=str,
                                             default=None))

            pass1 = request.form.get('robotPassword', type=str, default=None)
            pass2 = request.form.get('robotPasswordConfirm',
                                     type=str,
                                     default=None)
            if pass1 is not None and pass1 == pass2:
                if pass1 != '':
                    Preferences.set('general', 'password', pass1)

            # Preferences.set('update', 'branch', request.form.get('updateBranch', type=str, default=None))
            # Preferences.set('update', 'auto_update',
            #                 request.form.get('updateAuto', type=str, default=None))

            Preferences.set('alive',
                            'enabled',
                            request.form.get('aliveEnabled',
                                             type=bool,
                                             default=False))
            # Preferences.set('alive', 'aliveness', request.form.get('aliveness', type=str, default=None))
            Preferences.set('alive', 'aliveness', 0)
            Preferences.set('alive',
                            'blink',
                            request.form.get('aliveBlink',
                                             type=bool,
                                             default=False))
            Preferences.set('alive',
                            'gaze',
                            request.form.get('aliveGaze',
                                             type=bool,
                                             default=False))

            Preferences.set('audio',
                            'master_volume',
                            request.form.get('volume', type=int))
            Preferences.set('audio',
                            'tts_engine',
                            request.form.get('ttsEngine',
                                             type=str,
                                             default=None))
            Preferences.set(
                'audio',
                'tts_language',
                request.form.get('ttsLanguage', type=str, default=None))
            Preferences.set('audio',
                            'tts_gender',
                            request.form.get('ttsGender',
                                             type=str,
                                             default=None))

            Preferences.set('wireless',
                            'ssid',
                            request.form.get('wirelessSsid',
                                             type=str,
                                             default=None))
            Preferences.set('wireless',
                            'channel',
                            request.form.get('wirelessChannel', type=int))

            if request.form.get('wirelessSamePass', None) == 'on':
                # Set to same password
                Preferences.set('wireless', 'password', Preferences.get(
                    'general', 'password', 'RobotOpsoro'))
            else:
                pass1 = request.form.get('wirelessPassword',
                                         type=str,
                                         default=None)
                pass2 = request.form.get('wirelessPasswordConfirm',
                                         type=str,
                                         default=None)
                if pass1 is not None and pass1 == pass2:
                    if pass1 != '':
                        Preferences.set('wireless', 'password', pass1)

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
            'update': {
                'available': Preferences.check_if_update(),
                'branch': Preferences.get('update', 'branch',
                                          Preferences.get_current_branch()),
                # 'branches': Preferences.get_remote_branches(),
                'autoUpdate': Preferences.get('update', 'auto_update', False)
            },
            'alive': {
                'enabled': Preferences.get('alive', 'enabled', False),
                'aliveness': Preferences.get('alive', 'aliveness', '0'),
                'blink': Preferences.get('alive', 'blink', True),
                'gaze': Preferences.get('alive', 'gaze', True)
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

        print_info(data)

        return opsoroapp.render_template(config['formatted_name'] + '.html', **data)

    @app_bp.route('/update', methods=['GET', 'POST'])
    @opsoroapp.app_view
    def update():
        Preferences.update()

    opsoroapp.register_app_blueprint(app_bp)


def setup(opsoroapp):
    pass


def start(opsoroapp):
    pass


def stop(opsoroapp):
    pass
