from __future__ import with_statement

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory

from opsoro.console_msg import *
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.expression import Expression
from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread
from opsoro.users import Users

import time

from functools import partial
import os

import json
import urllib2
from functools import partial
from random import randint

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)
get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

config = {
    'full_name':            'Facebook Live',
    'icon':                 'fa-video-camera',
    'color':                'red',
    'difficulty':           3,
    'tags':                 ['template', 'developer'],
    'allowed_background':   False,
    'connection':           Robot.Connection.OFFLINE,
    'activation':           Robot.Activation.AUTO
}
config['formatted_name'] =  config['full_name'].lower().replace(' ', '_')

thread_fb_t = None
fb_params_stringified = None
secOphalenData = 5

def thread_fb():
    time.sleep(0.05)  # delay
    global thread_fb_t
    global fb_params_stringified
    print_info(fb_params_stringified)
    while not thread_fb_t.stopped():
        send_data('threadRunning', fb_params_stringified)
        time.sleep(secOphalenData)
        pass

def send_data(action, data):
    Users.send_app_data(config['formatted_name'], action, data)

def handlePostData(data):
    global thread_fb_t
    global fb_params_stringified
    fb_params_stringified = json.loads(data) #doesn't need to be parsed to json because we'll send it back to the js instantly or does it just for python??
    print_info(fb_params_stringified)
    thread_fb_t = StoppableThread(target=thread_fb)



def setup_pages(server):
    app_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')


    @app_bp.route('/')
    @server.app_view
    def index():
        data = {
            'actions': {},
            'data': [],
            'emotions': []
        }
        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        data['emotions'] = Expression.expressions

        return server.render_template(config['formatted_name'] + '.html', **data)


    @app_bp.route('/', methods=['POST'])
    @server.app_view
    def post():
        data = {'actions': {}, 'emotions': [], 'sounds': []}

        if request.form['action'] == 'postToThread':
            if request.form['data']:
                handlePostData(request.form['data'])

        if request.form['action'] == 'stopThread':
            global thread_fb_t
            if thread_fb_t != None:
                thread_fb_t.stop()

            print_info("thread stopped")

        return server.render_template(config['formatted_name'] + '.html', **data)

    server.register_app_blueprint(app_bp)

# Default functions for setting up, starting and stopping an app
def setup(server):
    pass

def start(server):
    pass

def stop(server):
    thread_fb_t.stop()
    pass
