from __future__ import with_statement

import json, datetime
import json,datetime

import time
import glob
import requests

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from threading import Thread, current_thread
from functools import partial

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.users import Users
from opsoro.expression import Expression
from opsoro.stoppable_thread import StoppableThread
from opsoro.sound import Sound
from opsoro.module.eye import Eye
from opsoro.preferences import Preferences


import os

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

clientconn = None

config = {
    'full_name':            'personal assistant',
    'icon':                 'fa-child',
    'color':                'blue',
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
        #Opslaan van de activity
        save_activity(data)
        #De data die verkregen is via de webhook laten uitspreken
        speak(data)
       
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

    #ophalen expressions
    @app_bp.route('/getreactions',methods=['GET'])
    def getreactions():
        data = {
            'expressions': Expression.expressions,
        }
        return jsonify(data)
    
    #ophalen sounds
    @app_bp.route('/getsounds',methods=['GET'])
    def getsounds():
        filenames = glob.glob(get_path('../../data/sounds/*.wav'))
        data = {
            'sounds': []
        }
        for filename in filenames:
            data['sounds'].append(os.path.split(filename)[1])
        data['sounds'].sort()
        
        return jsonify(data)
    
    #save applet
    @server.app_socket_message('saveapplet')
    def saveApplet(conn, data):
        filename = os.path.join(app_bp.static_folder+'/json/', 'Applets.json')      
        with open(filename, 'r') as read_file:
                json_data = json.load(read_file)
                json_data['Applets'].append(data['data']['applet'])   
        with open(filename, 'w') as write_file:
            write_file.write(json.dumps(json_data))
        response = {
            'data': "Applet added..."
        }
        Users.send_app_data(config['formatted_name'], "AppletAdded", response)
    
    #remove applet
    @server.app_socket_message('deleteapplet')
    def deleteApplet(conn,data):
        removed_applet = data['data']['applet-id']
        filename = os.path.join(app_bp.static_folder+'/json/', 'Applets.json')
        with open(filename, 'r') as read_file:
            json_data = json.load(read_file)
            applets = json_data['Applets']
            for applet in xrange(len(applets)):
                if applets[applet]["Applet_id"] == removed_applet:
                    applets.pop(applet)
                    break
            json_data['Applets'] = applets
        with open(filename, 'w') as write_file:
            write_file.write(json.dumps(json_data))
        response = {
            'data': removed_applet
        }
        Users.send_app_data(config['formatted_name'], "AppletRemoved", response)

    
    #toevoegen van command via websocket
    @server.app_socket_message('command')
    def socket_command(conn, data):
        global command_queue
        command_queue.append(data['data'])
        response = {
            'data': "Message received"
        }
        Users.send_app_data(config['formatted_name'], "MessageResponse", response)

    #verwijderen van command via websocket
    @server.app_socket_message('remove-command')
    def socket_remove_command(conn, data):
        global command_queue
        command_queue[:] = [command for command in command_queue if command.get('id') != data['data']['id']]
        response = {
            'data': "Command "+data['data']['id']+" removed"
        }
        Users.send_app_data(config['formatted_name'], "MessageResponse", response)



    @server.app_socket_connected
    def socket_connected(conn):
        global clientconn
        clientconn = conn
        print_info("Connected")
    
    @server.app_socket_disconnected
    def socket_disconnected(conn):
        global clientconn
        clientconn = None
        print_info("Disconnected")


    #Activity opslaan in de json file
    def save_activity(data):
        data['date'] = str(datetime.date.today())
        data['time'] = str(datetime.datetime.now().strftime("%H:%M:%S"))
        print_info(data)
        Users.send_app_data(config['formatted_name'], "MessageInComing", data)
        filename = os.path.join(app_bp.static_folder+'/json/', 'Activity.json')
        if os.path.exists(filename):
            with open(filename, 'r') as read_file:
                json_data = json.load(read_file)
                if len(json_data['Activity']) == 20 :
                    del json_data['Activity'][:1]
                json_data['Activity'].append(data)   
            with open(filename, 'w') as write_file:
                write_file.write(json.dumps(json_data))
        else: #create activity.json if not exists
            with open(filename, 'w+') as write_new_file:
                json_data['Activity'].append(data)
                write_new_file.write(json.dumps(json_data))

    #Data lezen van json file
    def read_json_file(filename):
        try:
            filename = os.path.join(app_bp.static_folder+'/json/',filename)
            if os.path.exists(filename):
                with open(filename) as json_file:
                        json_read = json.load(json_file)
                        return json_read
            else:
                print_info("No such file")
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
        Sound.wait_for_sound()
    print_info("Alarm stopped...")
    return

#commands uitvoeren en dan verwijderen van de queue
def CommandLoop():
    print_info('Start Command loop')
    global command_queue
    time.sleep(1)
    while not command_webservice.stopped():
        if len(command_queue) > 0:
            
            command = command_queue.pop(0)
            print_info(command)
            Expression.set_emotion_name(command['command-expression'])
            if command['command-hasSound']:
                Sound.play_file(command['command-sound'])
            #ifttt command
            if command['command-type'] == "ifttt":
                data = {
                     "value1": command['command-message']
                }
                requests.post("https://maker.ifttt.com/trigger/"+command['command-eventname']+"/with/key/b4mn_DZW0F-ERF-VIpE3r",data)  
            if command['command-hasTTS']:
                Sound.wait_for_sound()
                Sound.say_tts(command['command-say'])
                Sound.wait_for_sound()
                if command['command-type'] == "emotion":
                    Sound.say_tts(command['command-expression'])
                if command['command-type'] == "sound":
                    Sound.play_file(command['command-message'])
                if command['command-type'] == "ifttt":
                    Sound.say_tts(command['command-message'])                                   
            #do something
            response = {
                'data': "Remove"
            }
            Users.send_app_data(config['formatted_name'], "MessageCommand", response)
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
    #Sound.say_tts("Hello, my name is " + Preferences.get('general','robot_name','Robot'))
    global command_webservice
    command_webservice = StoppableThread(target=CommandLoop)

def stop(server):
    print_info('Stop Command loop')
    global command_webservice
    command_webservice.stop()
