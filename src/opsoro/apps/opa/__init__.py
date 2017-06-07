from __future__ import with_statement

import paho.mqtt.client as mqtt
import json, datetime
import json,datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, jsonify

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.expression import Expression
# from opsoro.stoppable_thread import StoppableThread
from opsoro.sound import Sound
from opsoro.preferences import Preferences
from functools import partial

import os

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

clientconn = None

config = {
    'full_name':            'opsoro personal assistant',
    'icon':                 'fa-child',
    'color':                'green',
    'difficulty':           1,
    'tags':                 ['template', 'developer'],
    'allowed_background':   False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] =  'opa'

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
            'activity': [],
        }

        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)
       
        filename = os.path.join(app_bp.static_folder, 'Applets.json')
        with open(filename) as blog_file:
            json_data = json.load(blog_file)

        filename = os.path.join(app_bp.static_folder, 'Commands.json')
        with open(filename) as blog_file:
            json_commands = json.load(blog_file)

        filename = os.path.join(app_bp.static_folder, 'Activity.json')
        with open(filename) as activity_file:
            activity_data = json.load(activity_file)

        data['data'] = json_data
        data['commands'] = json_commands
        data['activity'] = activity_data
        return server.render_template(config['formatted_name'] + '.html', **data)

        filename = os.path.join(app_bp.static_folder, 'Activity.json')
        with open(filename) as activity_file:
            activity_data = json.load(activity_file)
        data['data'] = json_data
        data['activity'] = activity_data
        print_info(data['activity'])
        return server.render_template(config['formatted_name'] + '.html', **data)

    @app_bp.route('/action', methods=['POST'])
    def action():
        json_dict = request.data
        data = json.loads(json_dict)
        print_info(data)

        speak(data)
        save_activity(data)
        return jsonify(data)
        
    @app_bp.route('/name', methods=['POST'])
    def change_name():
        data = {}
        if request.method == 'POST':
            Preferences.set('general', 'robot_name', request.form.get('robotName', type=str, default=None))
        return redirect('/apps/opa/')

    
    @server.app_socket_message('Message')
    def s_key_up(conn, data):
        print_info("Message received")
        print_info(str(data))
        data = {
            'data': "Hello back"
        }
        conn.send_data("Message",data)

    @server.app_socket_connected
    def socket_connected(conn):
        print_info("Connected")
    
    @server.app_socket_disconnected
    def socket_connected(conn):
        print_info("Disconnected")



    def save_activity(data):
        data['date'] = str(datetime.date.today())
        data['time'] = str(datetime.datetime.now().strftime("%H:%M:%S"))
        print_info(data)
        filename = os.path.join(app_bp.static_folder, 'Activity.json')
        with open(filename, 'r') as blog_file:
            json_data = json.load(blog_file)
            json_data['Activity'].append(data)
            print_info(json_data)    
        with open(filename, 'w') as write_file:
            write_file.write(json.dumps(json_data))     


    server.register_app_blueprint(app_bp)


def speak(data):
    if data['service'] != "Alarm":
        if data['say'] == "True":
            play_data = data['play']
            Sound.play_file("smb_1-up.wav")
            Sound.wait_for_sound()
        else: print_info('No need to play')
    else:
        print_info("Alarm")
        alarm()
    print_info("Exit speak action..")
    return


def play(play_data):
    Sound.say_tts(play_data['1'])
    Sound.wait_for_sound()
    Sound.say_tts(play_data['2'])
    Sound.wait_for_sound()

    Sound.say_tts(play_data['3'])

    Sound.say_tts(play_data['play3'])


def alarm():
    onetoten = range(0,3)
    for i in onetoten:
        Sound.play_file("1_kamelenrace.wav")
        Sound.wait_for_sound()
    print_info("Alarm stopped...")
    return


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
