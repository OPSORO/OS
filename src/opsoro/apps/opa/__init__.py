from __future__ import with_statement

import json, datetime
import json,datetime

import time
from threading import Thread, current_thread

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, jsonify

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.expression import Expression
from opsoro.stoppable_thread import StoppableThread
from opsoro.sound import Sound
from opsoro.module.eye import Eye
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
        Robot.sleep()
        Robot.blink(1)
        
       #json data ophalen uit json-files 
        json_commands = read_json_file('Commands.json')
        activity_data = read_json_file('Activity.json')
        
        #json data doorsturen naar template
        data['commands'] = json_commands
        data['activity'] = activity_data['Activity'][-10:]

        return server.render_template(config['formatted_name'] + '.html', **data)

    #IFTTT Maker Webhook web request opvangen
    @app_bp.route('/action', methods=['POST'])
    def action():
        Robot.wake()
        json_dict = request.data
        data = json.loads(json_dict)
        print_info(data)
        
        #De data die verkregen is via de webhook laten uitspreken
        speak(data)

        #Opslaan van de activity
        save_activity(data)
        Robot.sleep()
        return jsonify(data)
        
    #Naam veranderen van persoon die de robot gebruikt WIP
    @app_bp.route('/name', methods=['POST'])
    def change_name():
        data = {}
        if request.method == 'POST':
            Preferences.set('general', 'robot_name', request.form.get('robotName', type=str, default=None))
        return redirect('/apps/opa/')

    #ophalen applets via GET
    @app_bp.route('/getapplets',methods=['GET'])
    def getapplets():
        json_data = read_json_file('Applets.json')
        return jsonify(json_data)

    #ophalen commands via GET
    @app_bp.route('/getcommands',methods=['GET'])
    def getcommands():
        json_data = read_json_file('Commands.json')
        return jsonify(json_data)
        
    

    @server.app_socket_message('command')
    def socket_message(conn, data):
        print_info(data)
        #global command_queue
        print_info("Message received")
        #command_queue = data['data']
        #command_queue.remove('placeholder')
        #print_info(command_queue)
        response = {
            'data': "Message received"
        }
        conn.send_data("Message",response)

    @server.app_socket_connected
    def socket_connected(conn):
        global clientconn
        clientconn = conn
        print_info("Connected")
    
    @server.app_socket_disconnected
    def socket_connected(conn):
        global clientconn
        clientconn = None
        print_info("Disconnected")


    #Activity opslaan in de json file
    def save_activity(data):
        data['date'] = str(datetime.date.today())
        data['time'] = str(datetime.datetime.now().strftime("%H:%M:%S"))
        print_info(data)
        filename = os.path.join(app_bp.static_folder+'/json/', 'Activity.json')
        with open(filename, 'r') as blog_file:
            json_data = json.load(blog_file)
            json_data['Activity'].append(data)   
        with open(filename, 'w') as write_file:
            write_file.write(json.dumps(json_data))

    #Data lezen van json file
    def read_json_file(filename):
        try:
            filename = os.path.join(app_bp.static_folder+'/json/',filename)
            with open(filename) as json_file:
                json_read = json.load(json_file)
                return json_read
        except:
            print_error('Failed to read json file')
            return null  


    server.register_app_blueprint(app_bp)

#Uitvoeren van spraak
def speak(data):
    if data['service'] != "Alarm":
        if data['say'] == "True":
            play_data = data['play']
            Sound.play_file("smb_1-up.wav")
            Sound.wait_for_sound()
            play(play_data)
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

#Alarm laten afspelen WIP
def alarm():
    onetoten = range(0,3)
    for i in onetoten:
        Sound.play_file("1_kamelenrace.wav")
        Sound.wait_for_sound(print_info)
    print_info("Alarm stopped...")
    return

def CommandLoop():
    print_info('Start Command loop')
    global command_queue
    time.sleep(1)
    while not command_webservice.stopped():
        if len(command_queue) > 0:
            print_info(command_queue.pop(0))
            #do something
            response = {
                'data': "Remove"
            }
            clientconn.send_data("Message",response)
        command_webservice.sleep(5)

def demo():
    # publicly accessible function
    if 1 > 0:
        return {'status': 'success'}
    else:
        return {'status': 'error', 'message': 'This is a demo error!'}

# Default functions for setting up, starting and stopping an app
def setup(server):
    global command_queue
    command_queue = []

def start(server):
    Sound.say_tts("Hello, my name is " + Preferences.get('general','robot_name','Robot'))
    global command_webservice
    command_webservice = StoppableThread(target=CommandLoop)

def stop(server):
    print_info('Stop Command loop')
    global command_webservice
    command_webservice.stop()
